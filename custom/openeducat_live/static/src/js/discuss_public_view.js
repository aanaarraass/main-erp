/** @odoo-module **/
import { registerInstancePatchModel } from '@mail/model/model_core';
import { clear, insertAndReplace, link } from '@mail/model/model_field_command';

registerInstancePatchModel('mail.discuss_public_view', "openeducat_live/static/src/js/discuss_public_view.js", {
    async switchToThreadView() {
        this.update({
            threadViewer: insertAndReplace({
                extraClass: 'flex-grow-1',
                hasMemberList: true,
                hasThreadView: true,
                hasTopbar: true,
                thread: link(this.channel),
            }),
            welcomeView: clear(),
        });
        if (this.isChannelTokenSecret) {
            // Change the URL to avoid leaking the invitation link.
            window.history.replaceState(window.history.state, null, `/discuss/channel/${this.channel.id}${window.location.search}`);
        }
        if (this.channel.defaultDisplayMode === 'video_full_screen') {
            await this.channel.toggleCall({ startWithVideo: true });
            setTimeout(() => {
                if (this.threadView) {
                    if (this.threadView.rtcCallViewer) {
                        this.threadView.rtcCallViewer.activateFullScreen();
                    }
                }
            }, 100);
        }
    }
}); 
