$(function () {
  $('#get_captcha').click(function (event) {
    // 阻止原生的提交
    event.preventDefault();
    var email = $('input[name=email]').val();
    if (!email) {
      xtalert.alertInfoToast('请输入邮箱');
      return;
    }

    iqajax.get({
      'url': '/backend/email_captcha/',
      'data': {
        'email': email
      },
      'success': function (data) {
        if (data['code'] === 200) {
          xtalert.alertSuccessToast(data['message']);
        } else {
          xtalert.alertInfo(data['message']);
        }
      },
      'fail': function (error) {
        xtalert.alertNetworkError();
      }
    })
  });

  $('#submit').click(function (event) {
    event.preventDefault();
    var emailE = $('input[name=email]');
    var captchaE = $('input[name=captcha]');

    var email = emailE.val();
    var captcha = captchaE.val();

    iqajax.post({
      'url': '/backend/resetemail/',
      'data': {
        'email': email,
        'captcha': captcha
      },
      'success': function (data) {
        if (data['code'] === 200) {
          xtalert.alertSuccessToast(data['message']);
          emailE.val('');
          captchaE.val('');
          setTimeout(function () {
            window.location.href = '/backend/login/'
          }, 3000)
        } else {
          xtalert.alertInfo(data['message']);
        }
      },
      'fail': function (error) {
        xtalert.alertNetworkError();
      }
    })
  })
});