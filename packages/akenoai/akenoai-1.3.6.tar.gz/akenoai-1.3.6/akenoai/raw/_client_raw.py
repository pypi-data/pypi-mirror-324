# created by @xtdevs

from pyrogram import Client
from pyrogram.raw import functions


class RawFunctions:
    def __init__(self, class_client=Client):
        self.client = class_client
        self.functions_ = functions

    async def _invoke_with_peer(self, func, peers=None, results_updates=False, **kwargs):
        peer = await self.client.resolve_peer(peers)
        results = await self.client.invoke(func(peer=peer, **kwargs))
        return results if results_updates else None

    async def reactions(self, peers=None, results_updates=False):
        return await self._invoke_with_peer(
            self.functions_.messages.ReadReactions,
            peers, results_updates
        )

    async def mention_and_tags(self, peers=None, results_updates=False):
        return await self._invoke_with_peer(
            self.functions_.messages.ReadMentions,
            peers, results_updates
        )

    async def send_screenshot_notification(self, peers=None, results_updates=False):
        return await self._invoke_with_peer(
            self.functions_.messages.SendScreenshotNotification,
            peers, results_updates,
            reply_to_msg_id=0,
            random_id=self.client.rnd_id()
        )
