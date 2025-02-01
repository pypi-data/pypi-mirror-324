from pydantic import BaseModel
from nonebot.adapters.onebot.v11 import GroupMessageEvent

class Config(BaseModel):

    gif_fps: int = 30
    total_duration: int = 2
    max_turns: int = 4
    rotation_direction: int = -1

    params: dict[str, list[str]] = {"skip_gif": ["-s", "s", "stop"]}
    self_params: dict[str, list[str]] = {"self_join": ["我", "自己"]}
    background_params: dict[str, list[str]] = {"background.gif": ["default"]}
    join_commands: dict[str, list[str]] = {"加入": ["旅行伙伴加入", "旋转"]}
        
    @staticmethod
    async def rule(event: GroupMessageEvent) -> bool:
        msg = event.get_message()
        return next(
            (msg_seg.data["qq"] != "all" for msg_seg in msg if msg_seg.type == "at"),
            False,
        )

    @staticmethod
    async def get_at(event: GroupMessageEvent) -> str:
        msg = event.get_message()
        return next(
            (
                "寄" if msg_seg.data["qq"] == "all" else str(msg_seg.data["qq"])
                for msg_seg in msg
                if msg_seg.type == "at"
            ),
            "寄",
        )


