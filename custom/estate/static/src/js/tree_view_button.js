odoo.define('coordination_center.tree_view_button', function (require) {
    "use strict";
    var core = require('web.core');
    var ListView = require('web.ListView');
    var QWeb = core.qweb;
    ListView.include({
        render_buttons: function ($node) {
            var self = this;
            this._super($node);
            //自定义按钮click事件绑定处理方法
            this.$buttons.find('.o_list_tender_button_create').click(this.proxy('tree_view_action'));
        },
        /**
         * 实现自定义按钮的事件
         */
        tree_view_action: function () {
            console.log('点击事件！！！！');

        }
    });
});