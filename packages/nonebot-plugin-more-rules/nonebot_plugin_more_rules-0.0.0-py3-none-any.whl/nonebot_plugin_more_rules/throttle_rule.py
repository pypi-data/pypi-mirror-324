from datetime import datetime, timedelta
from typing import Optional, Union

from nonebot import on_message
from nonebot.internal.matcher import Matcher
from nonebot.rule import Rule
from nonebot.typing import T_RuleChecker


class ThrottleRule:
    """
    符合 nonebot.typing.T_RuleChecker 的检查器

    对发送消息进行节流
    """

    def __init__(
        self,
        days=0,
        seconds=0,
        microseconds=0,
        milliseconds=0,
        minutes=0,
        hours=0,
        weeks=0,
    ):
        self.interval = timedelta(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )
        self.last_call: datetime = None

    def __call__(self) -> bool:
        now = datetime.now()
        if self.last_call is None or now - self.last_call >= self.interval:
            self.last_call = now
            return True
        else:
            return False


def throttle(
    days=0,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=0,
    hours=0,
    weeks=0,
) -> Rule:
    """
    对发送消息进行节流
    """

    return Rule(
        ThrottleRule(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )
    )


def on_throttle(
    days=0,
    seconds=0,
    microseconds=0,
    milliseconds=0,
    minutes=0,
    hours=0,
    weeks=0,
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """
    注册一个消息事件响应器，并且当距离上次响应超过给定时间间隔时响应

    Args:
        interval: (timedelta): 节流时间间隔
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
        throttle(
            days=days,
            seconds=seconds,
            microseconds=microseconds,
            milliseconds=milliseconds,
            minutes=minutes,
            hours=hours,
            weeks=weeks,
        )
        & rule,
        **kwargs,
        _depth=_depth + 1,
    )
