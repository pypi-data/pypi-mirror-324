from nonebot.plugin import PluginMetadata

from .chain_rule import ChainRule, on_chain
from .pinyin_rule import PinyinRule, on_pinyin, pinyin, text_to_pinyin
from .throttle_rule import ThrottleRule, on_throttle, throttle

__plugin_meta__ = PluginMetadata(
    name="更多规则",
    description="更多符合 NoneBot2 规范的响应规则",
    usage="为其他插件编写提供功能",
    type="library",
    homepage="https://github.com/Drelf2018/nonebot-plugin-more-rules",
    supported_adapters={"~onebot.v11"},
)

__all__ = [
    "ChainRule",
    "on_chain",
    "PinyinRule",
    "on_pinyin",
    "pinyin",
    "text_to_pinyin",
    "ThrottleRule",
    "on_throttle",
    "throttle",
]
