from odoo import http
from odoo.http import request
from odoo.tools import config
import json
import os
from paramiko.proxy import subprocess


class mobileController(http.Controller):

    # 请求页面
    @http.route('/mobile/view', type='http', auth="public", csrf=False)
    def mobileView(self, mod=None, **kwargs):
        main = request.env['mobile.main'].sudo().search([])  # 可以根据需要添加过滤条件
        return request.render('mobile.mobile_view', {'main': main, 'quotations_count': len(main)})

    # 套餐价格查询
    @http.route('/mobile/price', type='json', auth="public", methods=['POST'], csrf=False)
    def requestPrice(self, mod=None, **kwargs):
        try:
            json_data = json.loads(request.httprequest.data)  # 手动解析JSON数据
        except json.JSONDecodeError:
            return request.make_response("Invalid JSON", status=400)
        # 价格查询逻辑
        print(json_data)
        data = {
            "services": "服务一",
            "combo": "套餐一",
            "month_of_purchase": "12",
            "price": "800",
            "total_price": "9600",
            "note": "无",
            "whitespace": "无"
        }
        # 返回JSON响应
        return data


    # 保存客户的套餐内容
    @http.route('/mobile/save_quotation', type='json', auth="public", methods=['POST'], csrf=False)
    def request(self, mod=None, **kwargs):
        # 解析参数
        try:
            json_data = json.loads(request.httprequest.data)  # 手动解析JSON数据
        except json.JSONDecodeError:
            return request.make_response("Invalid JSON", status=400)
        # 创建记录
        params = json_data.get('params',{})
        print(params)
        print(params.get('month_of_purchase'))
        record = request.env['mobile.main'].create({
            'services': params.get('services'),
            'combo': params.get('combo'),
            'month_of_purchase': params.get('month_of_purchase'),
            'price': params.get('price'),
            'total_price': params.get('total_price'),
            'note': params.get('note'),
            'whitespace': params.get('whitespace')
        })
        # 提交事务
        request.env.cr.commit()
        data = {
            "record_id": record.id
        }
        print('调用')
        print(record.id)
        return data

    # 返回预览的pdf文件
    @http.route('/mobile/responsePDF', type='http', auth="public", methods=['get'], csrf=False)
    def responsePDF(self, mod=None, **kwargs):
        # 获取URL参数
        id = kwargs.get('id')
        # 设置报告的URL
        request.env['ir.config_parameter'].sudo().set_param('report.url', 'http://127.0.0.1:8069')
        # 查询条件
        main = request.env['mobile.main'].sudo().search([('id', '=', id)])
        # 使用报告动作生成PDF
        pdf, _ = request.env.ref('mobile.test_process_view').sudo().render_qweb_pdf(main.id)
        pdf_file_path = os.path.join(config['data_dir'], 'reports', f'report_1.pdf')
        os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)  # 创建目录（如果不存在）

        # with open(pdf_file_path, 'wb') as f:
        #     f.write(pdf)
        return request.make_response(pdf, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Length', str(len(pdf))),
            ('Content-Disposition', 'inline; filename="report.pdf"')
        ])

    # 确认后生成pdf文件保存到后台
    @http.route('/mobile/upload_pdf', type='http', auth="public", methods=['POST'], csrf=False)
    def requestPDF(self, mod=None, **kwargs):
        file = request.httprequest.files.get('file')
        if file:
            # 保存文件到服务器
            file_path = os.path.join(config['data_dir'], 'reports', file.filename)  # 指定保存路径
            file.save(file_path)
            return request.make_response(json.dumps({'status': 'success', 'message': 'File uploaded successfully'}),
                                         headers=[('Content-Type', 'application/json')])
        else:
            return request.make_response(json.dumps({'status': 'error', 'message': 'No file uploaded'}),
                                         headers=[('Content-Type', 'application/json')])

        # 获取原始请求体并解析JSON数据

        # 设置报告的URL
        # request.env['ir.config_parameter'].sudo().set_param('report.url', 'http://127.0.0.1:8069')
        #
        # # 查询数据
        # main = request.env['mobile.main'].sudo().search([])
        # # 数据渲染PDF
        # pdf, _ = request.env.ref('mobile.action_quotation_view').sudo().render_qweb_pdf(main.ids)
        #
        # # 保存PDF到本地文件系统
        # # 命名规则
        # pdf_file_path = os.path.join(config['data_dir'], 'reports', f'report_1.pdf')
        # os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)  # 创建目录（如果不存在）
        # print(pdf_file_path)
        #
        # # 将PDF内容写入文件
        # with open(pdf_file_path, 'wb') as f:
        #     f.write(pdf)  # 写入PDF内容
        # print()
        # # 返回PDF文件
        # return (pdf_file_path)


    @http.route('/mobile/tView', type="http")
    def returnTestView(self, mod=None, **kwargs):
        # 渲染 QWeb 模板并返回 HTML 内容
        # report_obj = request.env['ir.actions.report']
        # report = report_obj._get_report_from_name('mobile.test_view')
        # html_content = report.render_qweb_pdf()[0]  # 获取 HTML 内容
        # pdf_file_path = os.path.join(config['data_dir'], 'reports', f'report_1.pdf')
        # os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)  # 创建目录（如果不存在）
        #
        # # 将PDF内容写入文件
        # with open(pdf_file_path, 'wb') as f:
        #     f.write(html_content)  # 写入PDF内容
        return request.render('mobile.test_service_context_view')
