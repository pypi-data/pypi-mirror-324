from functools import reduce
from typing import List, Optional, Union

from nonebot import on_message
from nonebot.adapters import Event
from nonebot.internal.matcher import Matcher
from nonebot.rule import Rule
from nonebot.typing import T_RuleChecker
from pypinyin import Style
from pypinyin import pinyin as pinyin_func


def text_to_pinyin(
    text: str,
    style: Style = Style.NORMAL,
    heteronym: bool = False,
) -> List[str]:
    """
    将文字转为对应拼音，多音字会以笛卡尔积形式给出

    Args:
        text (str): 要转换的文字
        style (Style, optional): 指定拼音风格
        heteronym (bool, optional): 是否启用多音字

    Returns:
        List[str]: 所有可能的字符串组合列表
    """
    text = text.strip()
    if text == "":
        return []
    return reduce(
        lambda old, new: [o + n for o in old for n in new],
        pinyin_func(text, style=style, heteronym=heteronym),
    )


class PinyinRule:
    """
    符合 nonebot.typing.T_RuleChecker 的检查器

    会检查消息纯文本转换为拼音后是否包含给定的字符串
    """

    def __init__(
        self,
        msg: str,
        style: Style = Style.NORMAL,
        heteronym: bool = False,
    ):
        self.msg = msg
        self.style = style
        self.heteronym = heteronym

    def __call__(self, event: Event) -> bool:
        for r in text_to_pinyin(event.get_plaintext(), self.style, self.heteronym):
            if self.msg in r:
                return True
        return False


def pinyin(
    msg: str,
    style: Style = Style.NORMAL,
    heteronym: bool = False,
) -> Rule:
    """
    匹配消息纯文本拼音

    Args:
        msg (str): 要匹配的拼音字符串
        style (Style, optional): 指定拼音风格
        heteronym (bool, optional): 是否启用多音字
    """
    return Rule(PinyinRule(msg, style=style, heteronym=heteronym))


def on_pinyin(
    msg: str,
    style: Style = Style.NORMAL,
    heteronym: bool = False,
    rule: Optional[Union[Rule, T_RuleChecker]] = None,
    _depth: int = 0,
    **kwargs,
) -> type[Matcher]:
    """
    注册一个消息事件响应器，并且当消息的纯文本拼音包含指定内容时响应

    Args:
        msg (str): 要匹配的拼音字符串
        style (Style, optional): 指定拼音风格
        heteronym (bool, optional): 是否启用多音字
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
        pinyin(msg, style=style, heteronym=heteronym) & rule,
        **kwargs,
        _depth=_depth + 1,
    )
