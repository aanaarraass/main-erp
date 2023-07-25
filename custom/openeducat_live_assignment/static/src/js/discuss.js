/** @odoo-module **/
import { registerInstancePatchModel } from '@mail/model/model_core';


registerInstancePatchModel('mail.discuss', "openeducat_live_assignment/static/src/js/discuss.js", {
    _created() {
        this._super(...arguments)
        this.openform = this.openform.bind(this);
    },
    openform() {
        var self = this
        if (this.thread) {
            this.env.services.rpc(
                {
                    route: '/mail/rtc/session/add-assignment',
                    params: {
                        channel_id: this.thread.id,
                    },
                },
                { shadow: true }
            ).then((res) => {
                var action = {
                    name: "Assignment",
                    type: 'ir.actions.act_window',
                    res_model: 'op.assignment',
                    views: [[false, 'form']],
                    target: 'new',
                    context: { 'default_course_id': res.course, 'default_batch_id': res.batch, 'default_subject_id': res.subject },
                };
                return this.env.bus.trigger('do-action', {
                    action
                });
            })
        }
    },
});
