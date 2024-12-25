odoo.define('custom_template_button_module.custom_button', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');

    var CustomButton = Widget.extend({
        events: {
            'click .o_button_upload_estate_customer': 'on_custom_button_click',
        },

        on_custom_button_click: function () {
            console.log('666')
        },
    });

    core.action_registry.add('custom_button_action', CustomButton);

    return CustomButton;
});
