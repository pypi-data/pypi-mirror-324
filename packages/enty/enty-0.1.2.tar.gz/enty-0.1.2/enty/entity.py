import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

from .utils import is_scalar_type, camel_to_snake

from dataclasses import fields, asdict, astuple
from typing import Any, List, Optional, Union, Type, Callable
from types import MappingProxyType

ENTITY_DEFAULTS = {
    'prefix': None,
    'suffix': None,
    'ident_sep': '____',
    'field_sep': '__',
    'make_dir': False,
    'base_dir': Path(),
    'append_class_sub_dir': True
}

def _init_dir(dir_to_init):
    logger.debug(f'[_init_dir] Initializing directory...')
    dir_to_init = Path(dir_to_init)
    if not dir_to_init.exists():
        logger.debug(f"[_init_dir] Directory does not exist. Creating.")
        dir_to_init.mkdir(parents=True)
    else:
        logger.debug(f"[_init_dir] Directory already exists. Skipping initialization.")


def _update_config(cls_or_self, update_dict=None, **kwargs):
    logger.debug(f"[_update_config] Updating config...")
    update_dict = {} if update_dict is None else update_dict
    update_dict.update(kwargs)
    cls_or_self._config.update(update_dict)
    logger.info(f"[update_config] config updated with {', '.join(f'{k}={v}' for k, v in update_dict.items())}")


def _compute_identity(cls_or_self, prefix=None, suffix=None):
    prefix = prefix if prefix is not None else cls_or_self.prefix
    suffix = suffix if suffix is not None else cls_or_self.suffix
    prefix_str = f"{prefix}_" if prefix is not None else ''
    suffix_str = f"_{suffix}" if suffix is not None else ''
    computed_identity = f"{prefix_str}{camel_to_snake(cls_or_self.class_name)}{suffix_str}"
    logger.debug(f"[{cls_or_self.class_name}.compute_identity] Computed identity: {computed_identity}")
    return computed_identity


def _compute_src_dir(cls_or_self, base_dir=None, sub_dir=None, src_dir=None, make_dir=None):
    logger.debug(f"[_compute_src_dir] --> start: {cls_or_self.class_name}")
    if src_dir is not None:
        dir_to_use = Path(src_dir)
        if base_dir is not None or sub_dir is not None:
            logger.warning(f"[{cls_or_self.class_name}.compute_src_dir] 'src_dir' provided. Ignoring 'base_dir' and 'sub_dir'.")
    else:
        logger.debug(f"[_compute_src_dir] src_dir not provided. Computing from base_dir and sub_dir.")
        dir_to_use = Path(base_dir) if base_dir is not None else Path(cls_or_self.base_dir)
        if sub_dir is not None:
            dir_to_use = dir_to_use / sub_dir
        elif cls_or_self.append_class_sub_dir:
            dir_to_use = dir_to_use / camel_to_snake(cls_or_self.class_name)
    logger.debug(f"[{cls_or_self.class_name}.compute_src_dir] Computed src_dir: {dir_to_use}")

    make_dir = make_dir if make_dir is not None else cls_or_self.make_dir
    if make_dir:
        _init_dir(dir_to_use)
    else:
        logger.debug(f"[_compute_src_dir] make_dir is False. Skipping directory initialization.")
    logger.debug(f"[_compute_src_dir] --> end: {cls_or_self.class_name}")
    return dir_to_use


class Identity(type):
    def __new__(mcs, name, bases, dct):
        logger.debug(f"[Identity __new__] --> start: {name} ")

        if name == "Entity":
            cls = super().__new__(mcs, name, bases, dct)
            cls._config = {**ENTITY_DEFAULTS}
            logger.debug(f"[Identity __new__] --> end: {name} ")
            return cls
        
        user_config_input = dct.pop('config', {})
        for k in ENTITY_DEFAULTS:
            if k in dct:
                user_config_input[k] = dct.pop(k)
        
        logger.debug(f'[Identity __new__] user supplied values extracted from dct: {user_config_input}')
        logger.debug(f'[Identity __new__] creating class {name} with dct: {dct}')
        
        cls = super().__new__(mcs, name, bases, dct)

        logger.debug(f'[Identity __new__] class {name} created. __dict__: {cls.__dict__}')

        if user_config_input:
            logger.debug(f'[Identity __new__] creating {name}._config from user supplied values.')
            cls._config = {**ENTITY_DEFAULTS, **user_config_input}
        elif hasattr(cls, '_config'):
            logger.debug(f'[Identity __new__] creating {name}._config with inherited _config.')
            cls._config = {**ENTITY_DEFAULTS, **cls._config}
        else:
            logger.debug(f'[Identity __new__] {name} has no config, creating with defaults.')
            cls._config = {**ENTITY_DEFAULTS}
        
        logger.debug(f'[Identity __new__] Initializing directories for {name}.')
        _compute_src_dir(cls)

        logger.debug(f'[Identity __new__] --> end: {name}')
        return cls

    @property
    def class_name(cls):
        return cls.__name__

    @property
    def config(cls):
        return MappingProxyType(cls._config)

    @property
    def src_dir(cls):
        return _compute_src_dir(cls)

    @property
    def identity(cls):
        return _compute_identity(cls)
    
    def __getattr__(cls, key):
        if key in ENTITY_DEFAULTS:
            return cls._config.get(key)
        # consider going back to traditional AttributeError message
        raise AttributeError(f"{cls.__name__} errored attempting to get {key}")

    def __setattr__(cls, key, value):
        if key in ENTITY_DEFAULTS:
            _update_config(cls, {key: value})
        else:
            super().__setattr__(key, value)

    def _parse_path(cls, path: Union[str, Path]) -> List[str]:
        """
        Split the stem of a path using the configured 'ident_sep'.
        The resulting list is typically [<identity>, <fields_str>].

        Parameters
        ----------
        path : str or Path
            The path whose filename's stem will be split.

        Returns
        -------
        list of str
            A list of tokens (usually two parts: identity, field-values).
        """
        filename = Path(path).stem
        parts = filename.split(cls.ident_sep)
        if len(parts) < 2:
            raise ValueError(f"Invalid path format: {path}. Expected separator '{cls.ident_sep}' not found.")
        logger.debug(f"[{cls.class_name}._parse_path] Path: {path}, "
                     f"Split parts: {parts}")
        return parts
    
    def init_from_path(cls, path: Union[str, Path]) -> Any:
        """
        Read a file path, validate its identity, parse field values, and construct
        an instance of the class with those values.

        Parameters
        ----------
        path : str or Path
            The path to parse into an Entity.

        Returns
        -------
        Any
            An instance of the class constructed with the parsed field values.

        Raises
        ------
        ValueError
            If the file's identity doesn't match this class's identity,
            or if the number of fields doesn't match.
        """
        parts = cls._parse_path(path)
        if len(parts) != 2:
            raise ValueError(f"Expected 2 parts from path '{path}', got {len(parts)}: {parts}")

        identity, fields_str = parts
        if identity != cls.identity:
            raise ValueError(f"File identity '{identity}' != class identity '{cls.identity}'")

        field_values = fields_str.split(cls.field_sep)
        logger.debug(f"[{cls.class_name}._read_path] Identity: {identity}, Field values: {field_values}")

        field_defs = []
        field_names = []
        field_types = []
        for f in fields(cls.Key):
            field_defs.append(f)
            field_names.append(f.name)
            field_types.append(f.type)

        if len(field_values) != len(field_names):
            raise ValueError(f"Mismatch in number of fields between class and path: "
                             f"{len(field_values)} vs {len(field_names)}")

        parsed_values = {}
        for fname, ftype, val in zip(field_names, field_types, field_values):
            # We assume a direct constructor call ftype(val) or something more nuanced if needed
            logger.debug(f"[{cls.class_name}._read_path] Parsing field: {fname}, Value: {val}, Type: {ftype}")
            try:
                parsed_values[fname] = ftype(val)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Error parsing field '{fname}' with value '{val}': {e}")

        logger.debug(f"[{cls.class_name}._read_path] Parsed values: {parsed_values}")
        return cls(**parsed_values)

    def view(cls, base_dir=None, sub_dir=None, src_dir=None) -> pd.DataFrame:
        """
        Collect all files in the source directory that match the class identity.

        Args:
            base_dir (str, optional): Override the default base directory.
            sub_dir (str, optional): Append a specific subdirectory to the base directory.
            src_dir (str, optional): Fully override the source directory.

        Returns:
            pd.DataFrame: Dataframe containing matching records.
        """
        # TODO: add cache support
        src_dir = _compute_src_dir(cls, base_dir=base_dir, sub_dir=sub_dir, src_dir=src_dir, make_dir=False)

        if not src_dir.exists():
            raise ValueError(f'Source directory does not exist: {src_dir}')
            
        logger.debug(f"[{cls.class_name}.view] Collecting objects from: {src_dir}")
        records = []

        skipped = 0
        for item in src_dir.iterdir():
            try:
                parts = cls._parse_path(item)
                if len(parts) == 2 and parts[0] == cls.identity:
                    logger.debug(f"[{cls.class_name}.view] Reading: {item}")
                    obj = cls.init_from_path(item)
                    records.append(obj.key_as_dict)
            except Exception as e:
                skipped += 1
                logger.error(f"[{cls.class_name}.view] Could not read {item}: {e}")
            else:
                skipped += 1
                logger.debug(f"[{cls.class_name}.view] Skipping item with mismatched identity: {item}")

        df = pd.DataFrame(records)
        logger.debug(f"[{cls.class_name}.view] Created DataFrame with {len(df)} records. {skipped} files skipped.")
        return df

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """
        If called with no arguments, return the view DataFrame.
        Otherwise, instantiate the class with provided arguments.

        Returns
        -------
        Any
        """
        if args or kwargs:
            logger.debug(f"[__call__] Creating instance of {cls.class_name} with args: {args}, kwargs: {kwargs}")
            return super().__call__(*args, **kwargs)
        return cls.view()



class Entity(metaclass=Identity):
    def __init__(self, 
        *args, 
        prefix=None,
        suffix=None,
        ident_sep=None,
        field_sep=None,
        make_dir=None,
        base_dir=None,
        append_class_sub_dir=None,
        **kwargs
    ):
        """
        
        """
        logger.debug(f"[Entity __init__] {self.__class__.__name__} --> start")
        user_config_input = self.__class__._config.copy()
        for k in ENTITY_DEFAULTS:
            v = locals().get(k)
            if v is not None:
                user_config_input[k] = v

        logger.debug(f"[Entity __init__]  args: {args}, kwargs: {kwargs} and config: {user_config_input}")
        self._config = user_config_input
        self.key = self.Key(*args, **kwargs)
        self.key_as_dict = asdict(self.key)
        self.key_as_tuple = astuple(self.key)

        # validate fields
        for fdef in fields(self.key):
            val = getattr(self.key, fdef.name)
            if not is_scalar_type(val):
                raise TypeError(
                    f"Field '{fdef.name}' must be scalar. "
                    f"Got {type(val).__name__}."
                )
        logger.debug(f"[Entity __init__] initializing directories for {self.__class__.__name__}.")
        _compute_src_dir(self)
        logger.debug(f"[Entity __init__] {self.__class__.__name__} --> end")

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def config(self):
        return MappingProxyType(self._config)

    @property
    def src_dir(self):
        return _compute_src_dir(self)

    @property
    def identity(self):
        return _compute_identity(self)

    def __getattr__(self, key):
        if key in ENTITY_DEFAULTS:
            return self._config.get(key)
        # consider going back to traditional AttributeError message
        raise AttributeError(f"{self.__class__.__name__} errored attempting to get {key}")

    def __setattr__(self, key, value):
        if key in ENTITY_DEFAULTS:
            _update_config(self, {key: value})
        else:
            super().__setattr__(key, value)

    def __repr__(self):
        return f'{self.class_name} object with key: {self.key.__repr__()}'
    
    def get_filename(self, ext=None, prefix=None, suffix=None, ident_sep=None, field_sep=None):
        """
        Construct a filename for this instance based on its class identity
        and its field values.

        Returns
        -------
        str
            The constructed filename.
        """
        vals = [str(getattr(self.key, f.name)) for f in fields(self.key)]
        identity = _compute_identity(self, prefix=prefix, suffix=suffix)
        ident_sep = ident_sep if ident_sep is not None else self.ident_sep
        field_sep = field_sep if field_sep is not None else self.field_sep
        name = f"{identity}{ident_sep}{field_sep.join(vals)}"
        
        if ext is not None:
            if not ext.startswith('.'):
                ext = f".{ext}"
            name += ext
        
        logger.debug(f"[{self.class_name}.get_filename] Constructed filename: {name}")
        return name

    def get_path(self, base_dir=None, sub_dir=None, src_dir=None, make_dir=None, ext=None, prefix=None, suffix=None, ident_sep=None, field_sep=None):
        """
        Construct a filesystem path for this instance based on its class identity
        and its field values.

        Parameters
        ----------
        base_dir : str or Path, optional
            The base directory. Defaults to the class's _base_dir if None.
        sub_dir : str, optional
            Subdirectory to append to the base directory.
        src_dir : str or Path, optional
            Fully override the source directory.
        make_dir : bool, optional
            Whether to create the directory if it doesn't exist.
        ext : str, optional
            File extension (e.g. '.txt'). If provided without a leading dot, one is added.
        prefix : str, optional
            String to prepend the filename with. Defaults to the class's prefix
        suffix : str, optional
            String to append to the end of the filename identity. Defaults to the class's suffix
        ident_sep : str, optional
            String to separate the filename identity from the filename fields. Defaults to the class's ident_sep
        field_sep : str, optional
            String to separate the field parameters in the filename. Defaults to the class's field_sep

        Returns
        -------
        Path
            The constructed path.
        """
        src_dir = _compute_src_dir(self, base_dir=base_dir, sub_dir=sub_dir, src_dir=src_dir, make_dir=make_dir)
        logger.debug(f"[{self.class_name}.get_path] Computed src_dir: {src_dir}")

        filename = self.get_filename(ext=ext, prefix=prefix, suffix=suffix, ident_sep=ident_sep, field_sep=field_sep)

        path = src_dir / filename
        logger.debug(f"[Entity.get_path] Computed path: {path}")
        return path


def entity(
    cls: Type[Any] = None,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    ident_sep: Optional[str] = None,
    field_sep: Optional[str] = None,
    make_dir: Optional[bool] = None,
    base_dir: Optional[Union[str, Path]] = None,
    append_class_sub_dir: Optional[bool] = None,
    config: Optional[dict] = None,
    config_proxy: Optional[MappingProxyType] = None,
) -> Callable[[Type[Any]], Type[Any]]:
    """
    Decorator function to convert a class into an Entity.

    Parameters
    ----------
    cls : Type[Any], optional
        The class being decorated. If None, returns a wrapper for delayed decoration.
    options : dict, optional
        entity configuration dict.
    **default_overrides
        Additional entity configuration overrides 

    Returns
    -------
    Callable[[Type[Any]], Type[Any]]
        A callable that, when given a class, returns a dataclass-augmented Entity.
    """
    logger.debug(f"[entity decorator] --> start.")

    user_config_input = {} if config is None else config
    logger.debug(f"[entity decorator] user provided config: {user_config_input}")
    for k in ENTITY_DEFAULTS:
        v = locals().get(k)
        if v is not None:
            logger.debug(f"[entity decorator] incorporating user provided keyword values: {k}={v}")
            user_config_input[k] = v
    logger.debug(f"[entity decorator] final user supplied config: {user_config_input}.")

    def wrapper(cls: Type[Any]) -> Type[Any]:
        logger.debug(f"[entity wrapper] --> start: {cls.__name__}.")

        if not issubclass(cls, Entity):
            logger.debug(f"[entity wrapper] {cls.__name__} is not a subclass of Entity. Creating a new {cls.__name__} that inherits from Entity and the user-defined {cls.__name__}.")
            new_cls = type(cls.__name__, (cls, Entity), dict(cls.__dict__))
            for k in ENTITY_DEFAULTS:
                if k in cls.__dict__:
                    logger.debug(f"[entity wrapper] deleting {k} from the original user-defined {cls.__name__}.__dict__")
                    delattr(cls, k)
        else:
            new_cls = cls

        logger.debug(f"[entity wrapper] new {new_cls.__name__} __dict__: {new_cls.__dict__}")

        if config_proxy is not None:
            new_cls._config = config_proxy
            logger.debug(f"[entity wrapper] config_proxy provided, replacing _config with proxy: {config_proxy}")
        
        elif user_config_input:
            new_cls._config = {**new_cls._config, **user_config_input}
            logger.debug(f"[entity wrapper] updating _config with values that user passed to decorator: {new_cls._config}")
        
        logger.debug(f"[entity wrapper] initializing directories for {new_cls.__name__}.")
        _compute_src_dir(new_cls)
        logger.debug(f"[entity wrapper] --> end: {cls.__name__}.")
        return new_cls

    logger.debug(f"[entity decorator] --> end.")
    if cls is not None:
        # Decorator used as @entity on a class with no parameters
        return wrapper(cls)
    return wrapper  # Decorator used as @entity(...) with parameters


class Schema:
    """
    Class-based decorator factory that configures and returns an entity decorator
    with a read-only proxy of identity defaults. This can be used to create 'schemas'
    that share a common configuration.
    """
    def __init__(
        self,     
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        ident_sep: Optional[str] = None,
        field_sep: Optional[str] = None,
        make_dir: Optional[bool] = None,
        base_dir: Optional[Union[str, Path]] = None,
        append_class_sub_dir: Optional[bool] = None,
        config: Optional[dict] = None
        ) -> None:
        """
        Parameters
        ----------
        **kwargs : Any
            Any configuration that should override default IDENTITY_DEFAULTS for this schema.
        """
        logger.debug(f'[Schema __init__] --> start')
        user_config_input = {} if config is None else config
        logger.debug(f"[Schema __init__] user provided config: {user_config_input}")
        for k in ENTITY_DEFAULTS:
            v = locals().get(k)
            if v is not None:
                logger.debug(f"[Schema __init__] incorporating user provided keyword values: {k}={v}")
                user_config_input[k] = v
        logger.debug(f"[Schema __init__] final user supplied config: {user_config_input}.")
        self._config = {**ENTITY_DEFAULTS, **user_config_input}
        logger.debug(f"[Schema __init__] Schema object constructed with _config={self._config}")
        logger.debug(f'[Schema __init__] --> end')

    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def config(self) -> MappingProxyType:
        return MappingProxyType(self._config)

    def __getattr__(self, key):
        if key in ENTITY_DEFAULTS:
            return self._config.get(key)
        # consider going back to traditional AttributeError message
        raise AttributeError(f"{self.__class__.__name__} errored attempting to get {key}")

    def __setattr__(self, key, value):
        if key in ENTITY_DEFAULTS:
            _update_config(self, {key: value})
        else:
            super().__setattr__(key, value)

    def update_config(self, update_dict=None, **kwargs):
        """
        Investigate adding this method to Entity as well.
        """

        update_dict = {} if update_dict is None else update_dict
        update_dict.update(kwargs)

        # Check if all keys in kwargs are valid
        invalid_keys = [key for key in update_dict if key not in ENTITY_DEFAULTS]
        if invalid_keys:
            raise ValueError(f"Invalid config keys: {', '.join(invalid_keys)}")

        # Update the config dictionary
        _update_config(self, update_dict)

    def __call__(self, cls: Type[Any]) -> Any:
        """
        Use this Schema as a decorator to produce an Entity. Merges the schema options
        with any dataclass overrides.

        Parameters
        ----------
        cls : Type[Any]
            The class to decorate.

        Returns
        -------
        Any
            The decorated class, or a wrapper for delayed decoration.
        """
        return entity(cls=cls, config_proxy=self.config)