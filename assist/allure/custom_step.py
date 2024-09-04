import collections
import re
import inspect
from functools import wraps, reduce
from allure_commons import plugin_manager
from allure_commons.utils import uuid4, represent


def _humanify(string_with_underscores, /):
    return re.sub(r'_+', ' ', string_with_underscores).strip()


def _fn_params_to_ordered_dict(func, *args, **kwargs):
    spec = inspect.getfullargspec(func)

    pos_or_named_ordered_names = list(spec.args)
    pos_without_defaults_dict = dict(zip(spec.args, args))
    if spec.args and spec.args[0] in ['cls', 'self']:
        pos_without_defaults_dict.pop(spec.args[0], None)

    received_args_amount = len(args)
    pos_or_named_not_set = spec.args[received_args_amount:]
    pos_defaults_dict = dict(zip(pos_or_named_not_set, spec.defaults or []))

    varargs = args[len(spec.args):]
    varargs_dict = {spec.varargs: varargs} if (spec.varargs and varargs) else {}
    pos_or_named_or_vargs_ordered_names = pos_or_named_ordered_names + [spec.varargs] if varargs_dict else pos_or_named_ordered_names

    pos_or_named_or_vargs_or_named_only_ordered_names = (
            pos_or_named_or_vargs_ordered_names
            + list(spec.kwonlyargs)
    )

    items = {
        **pos_without_defaults_dict,
        **pos_defaults_dict,
        **varargs_dict,
        **(spec.kwonlydefaults or {}),
        **kwargs,
    }.items()

    sorted_items = sorted(
        map(lambda kv: (kv[0], represent(kv[1])), items),
        key=lambda x: pos_or_named_or_vargs_or_named_only_ordered_names.index(x[0])
    )

    # Удаляем элемент 'element' из параметров
    filtered_items = {k: v for k, v in sorted_items if k != 'element'}

    return collections.OrderedDict(filtered_items)


class CustomStepContext:
    def __init__(
            self,
            title,
            params,
            display_params=True,
            params_separator=', ',
            derepresent_params=False,
            display_context=False,  # Отключаем отображение контекста класса
            translations=(),
    ):
        self.maybe_title = title
        self.params = params
        self.uuid = uuid4()
        self.display_params = display_params
        self.params_separator = params_separator
        self.derepresent_params = derepresent_params
        self.display_context = display_context
        self.translations = translations

    def __enter__(self):
        plugin_manager.hook.start_step(
            uuid=self.uuid,
            title=self.maybe_title or '',
            params=self.params)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plugin_manager.hook.stop_step(
            uuid=self.uuid,
            title=self.maybe_title or '',
            exc_type=exc_type,
            exc_val=exc_val,
            exc_tb=exc_tb)

    def __call__(self, func):
        @wraps(func)
        def impl(*args, **kw):
            __tracebackhide__ = True

            # Извлекаем параметр 'name' из аргументов
            name = kw.get('name', None)
            if name:
                step_title = f'{self.maybe_title} "{name}"'
            else:
                step_title = self.maybe_title

            params_dict = _fn_params_to_ordered_dict(func, *args, **kw)

            def derepresent(string):
                return string[1:-1]

            params_string = self.params_separator.join(
                list(map(derepresent, [str(value) for value in params_dict.values()]))
                if self.derepresent_params
                else [str(value) for value in params_dict.values()]
            )

            def title_to_display():
                return step_title or _humanify(func.__name__)

            name_to_display = title_to_display() + (': ' + params_string if params_string else '')

            translated_name = reduce(
                lambda text, item: text.replace(item[0], item[1]),
                self.translations,
                name_to_display
            ) if self.translations else name_to_display

            with CustomStepContext(translated_name, params_dict):
                return func(*args, **kw)

        return impl


def step(title):
    return CustomStepContext(title, {})