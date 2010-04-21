$(document).ready(function(){  
  $("a[@class=a_add_task]").click(
    function(){
        $(this).hide();
        $(this).parent("li").children("div").fadeIn('slow');
    }
  );
  $("input[@name=btn_add_task]").click(function(){add_task(this)});
  $("input[@name=btn_add_project]").click(function(){add_project(this)});
  $("input[@name=cbx_done_task]").change(function(){done_task(this)});
  $("a[@name=a_del_task]").click(function(){del_task(this)});
  $("a[@name=a_undone_task]").click(function(){undone_task(this)});
  $("a[@name=a_del_project]").click(function(){del_project(this)});
  $("a[@name=a_project_type]").click(function(){chg_project_type(this)});
});

function add_task(ev)
{
    var li =$(ev).parent("div");    
    var pid = li.children("input[@name=pid]");    
    var task_name = li.children("input[@name=task_name]");
    if(!task_name)
        alert('error');
    if (task_name && task_name.val() == "")
    {
        task_name.addClass('required');
        return;
    }    
    var priority = li.children("select[@name=priority]")
    //alert('pid:'+pid.val() + 'task_name:'+task_name.val() +'priority:' + priority.val());
    $.post('/todo/task/add/',
           {pid:pid.val(),task_name:task_name.val(), priority:priority.val()},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();
                    task_name.val('');
                    priority.val('0');
                }
                else
                    alert(ret);
           }           
           );
};

function add_project(ev){
    var li =$(ev).parent("li");
    var p_name = li.children("input[@name=project_name]");
    var p_type = li.children("input[@name=project_type]");
    if (p_name && p_name.val() == '')
    {
        p_name.addClass('required');
        return;
    }
    $.post('/todo/project/add/',
           {project_name:p_name.val(),project_type:p_type.attr("checked")?1:0},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();
                    p_name.val('');
                }
                else
                    alert(ret);
           }           
           );
};

function done_task(obj){
  obj = $(obj);
  if(obj.attr("checked"))
  {
    $.post('/todo/task/done/',
           {task_id:obj.val()},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();                    
                }
                else
                    alert(ret);
           }           
           );
  }
};

function del_task(obj){
  obj = $(obj);
  if(confirm('你真的要删除该task吗？'))
  {
    $.post('/todo/task/delete/',
           {task_id:obj.attr('rel')},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();                    
                }
                else
                    alert(ret);
           }           
           );
  }
};
//undone task
function undone_task(obj){
  obj = $(obj);
  $.post('/todo/task/undone/',
           {task_id:obj.attr('rel')},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();                    
                }
                else
                    alert(ret);
           }           
           );
};

function del_project(obj){
  obj = $(obj);
  if(confirm('你真的要删除该项目及项目下的所有任务吗？'))
  {
    $.post('/todo/project/delete/',
           {project_id:obj.attr('rel')},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();                    
                }
                else
                    alert(ret);
           }           
           );
  };
};

function chg_project_type(obj){
  obj = $(obj);
  var msg = '公共'
  if(obj.html().indexOf('public')>0)
    msg = '私有'    
   if(confirm('你真的要修改该项目为'+msg+'项目吗？'))
  {
    $.post('/todo/project/change_type/',
           {project_id:obj.attr('rel')},
           function(ret){
                if(ret == 'success')
                {
                    window.location.reload();                    
                }
                else
                    alert(ret);
           }           
           );
  }; 
};
function showCompleted()
{
    var div = $('#div_completed');
    if (div && div.css('display') == 'none')
      div.slideDown('slow');
    else
      div.slideUp('slow');
};