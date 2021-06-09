odoo.define('cloud_base.thread', function (require) {
"use strict";
    
    var core = require('web.core');
    var Thread = require('mail.widget.Thread');
    var _t = core._t;

    Thread.include({
        events: _.extend({}, Thread.prototype.events, {
            "click .o_attachment_download_from_cloud": "_onFileCloudDownload",
        }),
        _onFileCloudDownload: function (event) {
            // The method to request cloud for binary
            var self = this;
            var attachmentID = parseInt(event.target.id);
            this._rpc({
                model: "ir.attachment",
                method: 'upload_attachment_from_cloud_ui',
                args: [[attachmentID]],
            }).then(function (action) {
                self.do_action(action);
            });            
        },
    });

    return Thread

});
