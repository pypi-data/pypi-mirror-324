# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 常用工具封装，同步所有子模块新方法，保持公共模块的工具库最新版本
@created_time: 2022/6/15 14:14
"""

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request


# 流程调用装饰器
def flow_service_wrapper(func):
    """
    API 流程中间件装饰器
    PS 该装饰器必须配套request_params_wrapper 和 user_wrapper 一起使用
    PS 开放的服务必须使用key_value类型接收参数，如：params: dict = None, **kwargs
    """

    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    def wrapper(instance, arg_request=None, *args, request=None, request_params=None, user_info: dict = None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        :param user_info: 用户信息，使用用户登录验证装饰器才会生效。
        :param request_params: 请求参数解析
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request

        # ----------------- section 得到请求参数以及用户信息 start --------------------------
        user_info, is_pass = force_transform_type(variable=user_info, var_type="dict", default={})
        request_params, is_pass = force_transform_type(variable=request_params, var_type="dict", default={})
        # 自动补全，用户信息字段
        for k, v in user_info.items():
            request_params.setdefault(k, v)
        # ----------------- section 得到请求参数以及用户信息 end   --------------------------

        # ----------------- section 加载流程类,并判断是否要执行流程 start --------------------------
        CopyFlowProcessService, is_import = dynamic_load_class(import_path="xj_flow.services.flow_process_service", class_name="FlowProcessService")
        # 检查请求参数中是否由流程相关信息,判断是触发流程
        flow_node_id = request_params.pop("flow_node_id", None)
        flow_action_id = request_params.pop("flow_action_id", None)
        flow_node_value = request_params.pop("flow_node_value", None)
        flow_action_value = request_params.pop("flow_action_value", None)

        if is_import or (not flow_node_id and not flow_node_value) or (not flow_action_id and not flow_action_value):
            return func(instance, *args, request=request, request_params=request_params, user_info=user_info.copy(), **kwargs)
        # ----------------- section 加载流程类,并判断是否要执行流程 end   --------------------------

        service = CopyFlowProcessService()
        # ----------------- section 流程阻断判断 start --------------------------
        data, is_prevent = service.flow_switch(flow_node_id=flow_node_id, flow_node_value=flow_node_value)
        if is_prevent:
            from .custom_response import util_response
            return util_response(err=5000, msg=is_prevent)
        # ----------------- section 流程阻断判断 end   --------------------------

        # ----------------- section 执行前置流程方法 start --------------------------
        data, err = service.do_once_flow_in_service(
            flow_node_id=flow_node_id,
            flow_node_value=flow_node_value,
            flow_action_id=flow_action_id,
            flow_action_value=flow_action_value,
            source_params=request_params.copy(),
            run_mode="BEFORE"
        )
        # 如果有错误则计入执行错误日志
        if err:
            write_to_log(prefix="流程装饰器调用异常:", content=err)
        # 处理后的参数默认值补全
        data = data or {}
        request_params = data.get("source_params", request_params)
        # ----------------- section 执行前置流程方法 end   --------------------------

        # ----------------- section 执行接口方法 start --------------------------
        response = func(instance, *args, request=request, request_params=request_params.copy(), user_info=user_info.copy(), **kwargs)
        # 获取http响应的内容
        try:
            response_json = parse_json(response.content.decode(encoding="utf-8"))
            response_json, is_pass = force_transform_type(variable=response_json, var_type="dict", default={})
            response_err = response_json.detail("err", None)
            response_data, is_pass = force_transform_type(variable=response_json.detail("data", {}), var_type="only_dict", default={})
        except ValueError:
            response_json = {}
            response_err = None
            response_data = {}
        # ----------------- section 执行接口方法 end   --------------------------

        # ----------------- section 执行后置流程方法 start --------------------------
        if not response_err:
            # 如果请求接口没有报错则不可以执行
            request_params.update(response_data)
            data, err = service.do_once_flow_in_service(
                flow_node_id=flow_node_id,
                flow_node_value=flow_node_value,
                flow_action_id=flow_action_id,
                flow_action_value=flow_action_value,
                source_params=request_params.copy(),
                run_mode="AFTER"
            )
            if err:
                write_to_log(prefix="流程装饰器调用异常:", content=err)
        # ----------------- section 执行后置流程方法 end   --------------------------

        # ----------------- section 记录流程记录 start --------------------------
        # 流程完成记录
        if not response_err:
            data, flow_err = service.finish_flow(user_id=user_info.detail("user_id"))
            if flow_err:
                write_to_log(prefix="流程装饰器保存流程记录失败", content=flow_err)
        # 规则执行记录
        record, record_err = service.save_record(result_dict=response_json.get("data", {}), user_info=user_info.copy())
        if record_err:
            write_to_log(prefix="流程装饰器保存流程记录失败", content=record_err)
        # ----------------- section 记录流程记录 end   --------------------------
        return response

    return wrapper
