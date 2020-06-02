$(function () {
  $('#submit').click(function (event) {
    //阻止按钮默认的提交表单行为
    event.preventDefault();
    var oldpwdE = $('input[name=old_pwd]');
    var newpwdE = $('input[name=new_pwd]');
    var newpwd2E = $('input[name=new_pwd2]');

    var oldpwd = oldpwdE.val();
    var newpwd = newpwdE.val();
    var newpwd2 = newpwd2E.val();

    //这里使用我们自己封装好的iqajax，它具有了csrf
    iqajax.post({
      'url': '/backend/resetpwd/',
      'data': {
        'old_pwd': oldpwd,
        'new_pwd': newpwd,
        'new_pwd2': newpwd2
      },
      'success': function (data) {
        //根据状态码判断
        if (data['code'] === 200) {
          //弹出成功的提示框，提示语是从后台传过来的message
          xtalert.alertSuccessToast(data['message']);
          oldpwdE.val('');   //完成请求后把表单输入的值清空
          newpwdE.val('');
          newpwd2E.val('');
          setTimeout(function () {
            window.location.href = '/backend/login/'
          }, 3000);
        } else {
          xtalert.alertError(data['message']);
          oldpwdE.val('');
          newpwdE.val('');
          newpwd2E.val('');
        }
      },
      'fail': function (error) {
        xtalert.alertNetworkError('网络错误');
      }
    });
  });
});