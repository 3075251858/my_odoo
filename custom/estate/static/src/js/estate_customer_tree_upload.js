odoo.define('estate.upload.customer.mixin', function (require) {
"use strict";

    var core = require('web.core');
    var _t = core._t;

    var qweb = core.qweb;

    var UploadAttachmentMixin = {
        start: function () {
            // 定义一个唯一的fileUploadID(形如 my_file_upload_upload737)和一个回调方法
            this.fileUploadID = _.uniqueId('my_file_upload');
            $(window).on(this.fileUploadID, this._onFileUploaded.bind(this));
            return this._super.apply(this, arguments);
        },

        _onAddAttachment: function (ev) {
            // 一旦选择了附件，自动提交表单(关闭上传对话框)
            var input_main = $('input.o_input_file').val();
            console.log(input_main)
            if (input_main !== '') {
                 // o_estate_customer_upload定义在对应的QWeb模版中
                var $binaryForm = this.$('.o_estate_customer_upload form.o_form_binary_form');

                console.log(this.$el.find('.o_estate_customer_upload form.o_form_binary_form'))
                $binaryForm.submit();
            }
            console.log('110')
        },

        _onFileUploaded: function () {
            // 创建附件后的回调，根据附件ID执行相关处程序
            var self = this;
            var attachments = Array.prototype.slice.call(arguments, 1);
            // 获取附件ID
            var attachent_ids = attachments.reduce(function(filtered, record) {
                if (record.id) {
                    filtered.push(record.id);
                }
                return filtered;
            }, []);
            // 请求模型方法
            return this._rpc({
                model: 'estate.customer',  //模型名称
                method: 'create_customer_from_attachment', // 模型方法
                args: ["", attachent_ids],
                context: this.initialState.context,
            }).then(function(result) { // result为一个字典
                if (result.action_type == 'reload') {
                    self.trigger_up('reload'); // 实现在不刷新页面的情况下，刷新列表视图// 此处换成 self.reload(); 发现效果也是一样的
                } else if (result.action_type == 'do_action') {
                    self.do_action(result.action); // 执行action动作
                } else { // 啥也不做
                }
                // 重置 file input, 如果需要，可以再次选择相同的文件，如果不添加以下这行代码，不刷新当前页面的情况下，无法重复导入相同的文件
                self.$('.o_estate_customer_upload .o_input_file').val('');
             }).catch(function () {
                self.$('.o_estate_customer_upload .o_input_file').val('');
            });
        },

        _onUpload: function (event) {
            var self = this;
            // 如果隐藏的上传表单不存在则创建
            var $formContainer = this.$('.o_content').find('.o_estate_customer_upload');
            if (!$formContainer.length) {
                // estate.CustomerHiddenUploadForm定义在对应的QWeb模版中
                $formContainer = $(qweb.render('estate.CustomerHiddenUploadForm', {widget: this}))
                                                                         .appendTo($('.o_content'));
                $(".o_estate_customer_upload .o_form_binary_form").change(function(){
                    self._onAddAttachment();
                })
            }
            // 触发input选取文件
            $('.o_estate_customer_upload .o_input_file').click();
        },
    }
    return UploadAttachmentMixin;
});


odoo.define('estate.customer.tree', function (require) {
"use strict";
    var core = require('web.core');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var UploadAttachmentMixin = require('estate.upload.customer.mixin');
    var viewRegistry = require('web.view_registry');
    var AbstractField = require('web.AbstractField');

    var CustomListController = ListController.extend(UploadAttachmentMixin, {
        buttons_template: 'EstateCustomerListView.buttons',
        renderButtons: function () {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                var self = this;
                this.$buttons.on('click', '.o_button_upload_estate_customer', this.proxy('_onUpload'));
            }
        },
    });

    var CustomListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: CustomListController,
        }),
    });

    viewRegistry.add('estate_customer_tree', CustomListView);
});
