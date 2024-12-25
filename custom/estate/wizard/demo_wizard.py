#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from odoo import models, fields, api
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class DemoWizard(models.TransientModel):
    _name = 'demo.wizard'
    _description = 'demo wizard'

    property_id = fields.Many2one('estate.property', string='property')
    offer_ids = fields.One2many(related='property_id.offer_ids')

    def action_confirm(self):
        '''选中记录后，点击确认按钮，执行的操作'''

        #### 根据需要对获取的数据做相应处理
        # ... 获取数据，代码略(假设获取的数据存放在 data 变量中)

        record_ids = []
        for id, value_dict in data.items():
            record_ids.append(value_dict.get('data', {}).get('id'))
        if not record_ids:
            raise UserError('请选择记录')

        self.property_id.action_do_something(record_ids)
        return True

    @api.model
    def action_select_records_via_checkbox(self, args):
        '''通过wizard窗口界面复选框选取记录时触发的操作
        @params: args 为字典
        '''
        # ...存储收到的数据（假设仅存储data部分的数据），代码略

        return True  # 注意，执行成功则需要配合前端实现，返回True

    @api.model
    def default_get(self, fields_list):
        '''获取wizard 窗口界面默认值，包括记录列表 #因为使用了@api.model修饰符，self为空记录集，所以不能通过self.fieldName = value 的方式赋值'''

        res = super(DemoWizard, self).default_get(fields_list)
        record_ids = self.env.context.get(
            'active_ids')  # 获取当前记录ID列表(当前记录详情页所属记录ID列表) # self.env.context.get('active_id') # 获取当前记录ID

        property = self.env['estate.property'].browse(record_ids)
        res['property_id'] = property.id

        offer_ids = property.offer_ids.mapped('id')
        res['offer_ids'] = [(6, 0, offer_ids)]
        return res