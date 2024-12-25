odoo.define('estate.customer.fieldOne2Many', function (require) {
"use strict";
    var registry = require('web.field_registry');
    var FieldOne2Many = require('web.relational_fields').FieldOne2Many;
    var viewRegistry = require('web.view_registry');

    var MyFieldOne2Many = FieldOne2Many.extend({
        supportedFieldTypes: ['one2many'],
        events: _.extend({}, FieldOne2Many.prototype.events, {
            'click .display_action': '_on_your_button_clicked'
        }),

        // 重写渲染按钮函数，添加按钮
        _renderButtons: function () {
             this._super.apply(this, arguments);
             this.$buttons = $('<button type="button" name="action_confirm" class="btn btn-primary display_action">CustomButton</button>');
        },

        _on_your_button_clicked(){
            console.log('按钮点击');
            $("button[name='action_confirm']").attr("disabled", true);
        },
    });

    registry.add('my_field_one_2_many', MyFieldOne2Many)
});
