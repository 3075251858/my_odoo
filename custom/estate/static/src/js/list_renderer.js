function uuid() {
	var s = [];
	var hexDigits = "0123456789abcdef";
	for (var i = 0; i < 36; i++) {
		s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1);
	}
	s[14] = "4"; // bits 12-15 of the time_hi_and_version field to 0010
	s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1); // bits 6-7 of the clock_seq_hi_and_reserved to 01
	s[8] = s[13] = s[18] = s[23] = "-";

	var uuid = s.join("");
	return uuid;
}

odoo.define('estate.ListRenderer', function (require) {
    "use strict";

 	var ListRenderer = require('web.ListRenderer');
	ListRenderer = ListRenderer.extend({
	    init: function (parent, state, params) {
		    this._super.apply(this, arguments);
		    this.hasCheckBoxes = false;
			if ('hasCheckBoxes' in params.arch.attrs && params.arch.attrs['hasCheckBoxes']) {
                this.objectID = uuid();
                $(this).attr('id', this.objectID);

			    this.hasCheckBoxes = true;
			    this.hasSelectors = true;
			    this.records = {}; // 存放当前界面记录
			    this.recordsSelected = {}; // 存放选取的记录
			    this.modelName = undefined; // 定义点击列表复选框时需要访问的模型
			    this.modelMethod = undefined; // 定义点击列表复选框时需要调用的模型方法
			    this.jsMethodOnModelMethodDone = undefined; // 定义modelMethod方法执行完成后，需要调用的javascript方法
			    this.jsMethodOnToggleCheckbox = undefined; // 定义点击列表复选框时需要调用的javascript方法，比modelMethod优先执行


			    if ('modelName' in params.arch.attrs && params.arch.attrs['modelName']) {
			        this.modelName = params.arch.attrs['modelName'];
			    }
			    if ('modelMethod' in params.arch.attrs && params.arch.attrs['modelMethod']) {
			        this.modelMethod = params.arch.attrs['modelMethod'];
			    }
			    if ('jsMethodOnModelMethodDone' in params.arch.attrs && params.arch.attrs['jsMethodOnModelMethodDone']){
			        this.jsMethodOnModelMethodDone = params.arch.attrs['jsMethodOnModelMethodDone'];
			    }

			    if ('jsMethodOnToggleCheckbox' in params.arch.attrs && params.arch.attrs['jsMethodOnToggleCheckbox']) {
			        this.jsMethodOnToggleCheckbox = params.arch.attrs['jsMethodOnToggleCheckbox'];
			    }

                if ('saveSelectionsToSessionStorage' in params.arch.attrs && params.arch.attrs['saveSelectionsToSessionStorage']) {
			        this.saveSelectionsToSessionStorage = params.arch.attrs['saveSelectionsToSessionStorage'];
			    }
            }
		},
//		_onToggleSelection: function (ev) {
            // 点击列表表头的全选/取消全选复选框时会调用该函数
//		    this._super.apply(this, arguments);
//        },
        _onToggleCheckbox: function (ev) {
            if (this.hasCheckBoxes) {
                var classOfEvTarget = $(ev.target).attr('class');
                /* cstom-control-input 刚好点中复选框input,
                custom-control custom-checkbox 刚好点中复选框input的父元素div
                o_list_record_selector 点击到复选框外上述div的父元素*/
                if (['custom-control custom-checkbox', 'custom-control-input', 'o_list_record_selector'].includes(classOfEvTarget)){
                    if (this.jsMethodOnToggleCheckbox) {
                        eval(this.jsMethodOnToggleCheckbox)
                    }

                    var id = $(ev.currentTarget).closest('tr').data('id'); // 'custom-control-input' == classOfEvTarget
                    var checked = !this.$(ev.currentTarget).find('input').prop('checked') // 获取复选框是否框选 'custom-control-input' != classOfEvTarget
                    if ('custom-control-input' ==  classOfEvTarget) {
                        checked = this.$(ev.currentTarget).find('input').prop('checked')
                    }

                    if (id == undefined) {
                        if (checked == true) { // 全选
                            this.recordsSelected = JSON.parse(JSON.stringify(this.records));
                        } else { // 取消全选
                            this.recordsSelected = {};
                        }
                    } else {
                        if (checked == true) { // 勾选单条记录
                            this.recordsSelected[id] = this.records[id];
                        } else { // 取消勾选单条记录
                            delete this.recordsSelected[id];
                        }
                    }

                    if (this.saveSelectionsToSessionStorage) {
                        window.sessionStorage[this.objectID] = JSON.stringify(this.recordsSelected);
                    }

                    // 通过rpc请求模型方法，用于传输界面勾选的记录数据
                    if (this.modelName && this.modelMethod) {
                        self = this;
                        this._rpc({
                                model: this.modelName,
                                method: this.modelMethod,
                                args: [this.recordsSelected],
                            }).then(function (res) {
                                if (self.jsMethodOnModelMethodDone) {
                                    eval(self.jsMethodOnModelMethodDone);
                                }
                            });
                    }
                }
            }

            this._super.apply(this, arguments);

        },
        _renderRow: function (record) {
            // 打开列表页时会渲染行，此时存储渲染的记录
            if (this.hasCheckBoxes) {
                this.records[record.id] = {'data': record.data, 'context': record.context};
            }
            return this._super.apply(this, arguments);
        }

	});

odoo.__DEBUG__['services']['web.ListRenderer'] = ListRenderer; //覆盖原有的ListRender服务
});