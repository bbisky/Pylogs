tinyMCE.init({		
	        //mode : "textareas",  // Converts all textarea elements to editors when the page loads. 
	        mode:  "none" ,   //     Does not convert any elements. selectivity convert by markup option
		//elements : "content",
		theme : "advanced",
                skin : "o2k7",               
		plugins : "layer,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,visualchars,nonbreaking,xhtmlxtras,inlinepopups,filemanager,insertcode",
                height: "500",
                width: "80%",
        extended_valid_elements : "pre[class|name]",
        language:"zh",
		// Theme options
		theme_advanced_buttons1 : "newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,fontselect,fontsizeselect",
		theme_advanced_buttons2 : "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,filemanager,cleanup,|,insertdate,inserttime,preview,|,forecolor,backcolor,|,insertcode,code",
		theme_advanced_buttons3 : "",//"tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
		//theme_advanced_buttons4 : "insertlayer,moveforward,movebackward,absolute,|,styleprops,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,insertcode,filemanager",
		theme_advanced_toolbar_location : "top",
		theme_advanced_toolbar_align : "left",
		theme_advanced_statusbar_location : "bottom",
		theme_advanced_resizing : true
	});


window.onload = function(){
    var markup_select = document.getElementById('id_markup');
    if (markup_select){
	if (markup_select.value == "html"){
	    tinyMCE.execCommand('mceAddControl',false,'id_content')	    
	}
	addEvent(markup_select,'change',function(){
		if (markup_select.value != 'html'){
		    tinyMCE.execCommand('mceRemoveControl',false,'id_content')
		    //tinyMCE.get("id_content").hide()
		}else{
		    tinyMCE.execCommand('mceAddControl',false,'id_content')
		    //tinyMCE.get("id_content").show()
		}
	    }
	    )
    }
}