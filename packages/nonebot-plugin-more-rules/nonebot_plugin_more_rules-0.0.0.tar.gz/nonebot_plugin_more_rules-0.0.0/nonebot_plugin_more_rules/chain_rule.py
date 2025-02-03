from contextlib import AsyncExitStack
from typing import Optional, Union

from nonebot import on_message
from nonebot.dependencies import Dependent
from nonebot.internal.adapter import Bot, Event
from nonebot.internal.matcher import Matcher
from nonebot.rule import Rule
from nonebot.typing import T_RuleChecker, T_State


class ChainRule:
    """
    符合 nonebot.typing.T_RuleChecker 的检查器

    对检查器逐一判断
    """

    def __init__(self, *checkers: Union[T_RuleChecker, Dependent[bool]]) -> None:
        self.checkers: list[Dependent[bool]] = [
            (
                checker
                if isinstance(checker, Dependent)
                else Dependent[bool].parse(call=checker, allow_types=Rule.HANDLER_PARAM_TYPES)
            )
            for checker in checkers
        ]

    async def __call__(
        self,
        bot: Bot,
        event: Event,
        state: T_State,
        stack: Optional[AsyncExitStack] = None,
    ) -> bool:
        if not self.checkers:
            return True

        for checker in self.checkers:
            if not await checker(
                bot=bot,
                event=event,
                state=state,
                stack=stack,
                dependency_cache=None,
            ):
                return False

        return True


def on_chain(
    *checkers: Union[T_RuleChecker, Dependent[bool]],
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """
    注册一个消息事件响应器，并且当距离上次响应超过给定时间间隔时响应

    Args:
        checkers (Tuple[Union[T_RuleChecker, Dependent[bool]]]): 检查器链
        rule (Optional[Union[Rule, T_RuleChecker]], optional): 事件响应规则
        permission: 事件响应权限
        handlers: 事件处理函数列表
        temp: 是否为临时事件响应器（仅执行一次）
        expire_time: 事件响应器最终有效时间点，过时即被删除
        priority: 事件响应器优先级
        block: 是否阻止事件向更低优先级传递
        state: 默认 state
    """
    return on_message(
        Rule(ChainRule(*checkers)) & rule,
        **kwargs,
        _depth=_depth + 1,
    )
