function reload_verifycode(oVerifycode) {
    //var oVerifycode = document.getElementById(sVerifycode);
    var now = new Date();
	if (oVerifycode) {
        oVerifycode.src = "/utils/vcode/?date=" + now.getTime(); 
    }
}
function post_comment(){
  var btn = ':button.button';
  $(btn).attr('disabled',true);   
  var author = $.trim($('#id_comment_author').val());
  var  author_email=$.trim($('#id_comment_author_email').val());
  var  author_url=$.trim($('#id_comment_author_url').val());
  var  content=$.trim($('#id_comment_content').val());
  var  vcode=$.trim($('#id_comment_vcode').val());
  var validated = true;
  if(author == "")
  {
      input_error('#id_comment_author');
     validated = false;
  }
  else
  {
     $('#id_comment_author').css('border',"");
  }
  if(author_email == "")
  {
       input_error('#id_comment_author_email');
      validated = false;
  }
  else
  {
    var email_reg = /^[_\.0-9a-zA-Z+-]+@([0-9a-zA-Z]+[0-9a-zA-Z-]*\.)+[a-zA-Z]{2,4}$/;
    if(!email_reg.exec(author_email))
    {
       $('#id_comment_author_email').parent('div.form-row').append($('<span style="color:#f00;">请输入正确的EMAIL</span>'));
      validated = false;
    }
    else{
      $('#id_comment_author_email').css('border',"");
    }
  }
  if(content == "")
  {
       input_error('#id_comment_content');
       validated = false;
  } else
  {
     $('#id_comment_content').css('border',"");
  }
  if(vcode == "")
  {
       input_error('#id_comment_vcode');
       validated = false;
  }
   else
  {
     $('#id_comment_vcode').css('border',"");
  }
  
  if(!validated){
    $(btn).attr('disabled',false);    
  }
  else{
    var cmt_html = $('<li class="alt1"><strong>'+author+'</strong><span class="byline">发表于:'+new Date().toLocaleString()+'</span><p>'+content+'</p></li>');
    $.ajax({
       url: url,
       type: "POST",
       data: {author:author,
              email:author_email,
              url:author_url,
              content:content,
              vcode:vcode
              },
       dataType: "json",
       success: function(j){
            if(j.success){
                    alert(j.success)
                    reload_verifycode(document.getElementById('img_validate_code'));
                    $('form :text').val('');
                    $('form textarea').val('');
                    //append to page                    
                    if(!$('#comments>ul').length)
                    {             
                      $('div.post').after($('<div id="comments"><span class="commenttitle"><a name="comments"/>评论</span><ul></ul></div>'));
                    }
                     $('#comments>ul').append(cmt_html);
                }
                else
                    alert(j.error)
                $(btn).attr('disabled',false);
            },  
        error: function(XMLHttpRequest, textStatus, errorThrown){
            alert(textStatus +":" +errorThrown);
            $(btn).attr('disabled',false);
        }
       
     });
  }

}
function input_error(obj)
{
  $(obj).css('border',"1px solid #f00");
}