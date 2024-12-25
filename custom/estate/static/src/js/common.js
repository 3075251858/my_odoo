/*odoo.define('estate.customer.myTree', function (require) {
    "use strict";

    var ListController = require("web.ListController");
    var rpc = require("web.rpc");

    ListController.include({
        renderButtons: function($node){
            this._super.apply(this, arguments);
            var self = this;
            if (this.$buttons){
                this.$buttons.find(".oe_tiv_multi_create").on("click",function(){
                    self.do_action({
                        name: '文件上传',
                        res_model: 'upload.wizard',
                        views: [[false, 'form']],
                        type: 'ir.actions.act_window',
                        view_mode: 'form',
                        target: 'new',
                    });
                });
            }
        }
    })
});*/
odoo.define('my.ExcelUpload', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');


var QWeb = core.qweb;
var _t = core._t;

var MyUploadExcel = Widget.extend({
    template: 'my_uploadExcel',
    events: {
        "click .my_upload_button": "_onUploadAttachments",
        "change .my_chatter_attachment_form .o_form_binary_form": "_onAddAttachment",
    },
    /**
     * @override
     * @param {string} record.model
     * @param {Number} record.res_id
     * @param {Object[]} attachments
     */
    init: function (parent, record, attachments) {
        console.log('abc')
        this._super.apply(this, arguments);
        this.fileuploadId = _.uniqueId('oe_fileupload');
        $(window).on(this.fileuploadId, this._onUploaded.bind(this));
        this.currentResID = record.res_id;
        this.currentResModel = record.model;
        this.attachmentIDs = attachments;
        this.imageList = {};
        this.otherList = {};

        _.each(attachments, function (attachment) {
            // required for compatibility with the chatter templates.
            attachment.url = '/web/content/' + attachment.id + '?download=true';
            attachment.filename = attachment.datas_fname || _t('unnamed');
        });
        var sortedAttachments = _.partition(attachments, function (att) {
            return att.mimetype && att.mimetype.split('/')[0] === 'image';
        });
        this.imageList = sortedAttachments[0];
        this.otherList = sortedAttachments[1];
    },
    /**
     * @override
     */
    destroy: function () {
        $(window).off(this.fileuploadId);
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @param {Object} record
     */
    update: function (record) {
        this.currentResID = record.res_id;
        this.currentResModel = record.model;
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Method triggered when user click on 'add attachment' and select a file
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onAddAttachment: function (ev) {
        var $input = $(ev.currentTarget).find('input.o_input_file');
        if ($input.val() !== '') {
            var $binaryForm = this.$('form.o_form_binary_form');
            $binaryForm.submit();
        }
    },
    /**
     * @private
     * @param {MouseEvent} ev
     */
    /**
     * Opens File Explorer dialog if all fields are valid and record is saved
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onUploadAttachments: function (ev) {
        this.$('input.o_input_file').click();
    },
    /**
     * @private
     */
    _onUploaded: function(ev, response) {
        if (response.error) {
            this.do_warn(_t("Error"), _t("You are not allowed to upload an attachment here."));
        } else {
            this.trigger_up('reload_attachment_box');
        }
    },
});

return MyUploadExcel;

});

