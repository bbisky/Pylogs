/*
auto detect pre block and highlight it.
@author:sky
@date:2010-4-27
*/
getStyles = function(path) {
		var link = jQuery('<link>');
		jQuery("head").append(link);

		link.attr({
			rel: "stylesheet",
			type: "text/css",
			href: path
		});
	};
	
getScript = function(path, callback) {
		jQuery.ajax({
			async: false,
			type: "GET",
			url: path,
			success: function() {
                if(callback)
                    callback();
			},
			dataType: "script",
			cache: true
		});
	};
hl = function(){    
    SyntaxHighlighter.defaults['smart-tabs'] = false;
    SyntaxHighlighter.defaults['toolbar'] = false;
    SyntaxHighlighter.config.bloggerMode = true;
    SyntaxHighlighter.config.clipboardSwf = _media_root + '/js/sh/clipboard.swf';
    SyntaxHighlighter.all();
};
syntax_hl = function(){
    _aliases = {};
    _aliases["AS3"]=        ["as3","actionscript3"];
    _aliases["Bash"]=       ["bash","shell"];
    _aliases["ColdFusion"]= ["cf","coldfusion"];
    _aliases["CSharp"]=     ["c-sharp","csharp"];
    _aliases["Cpp"]=        ["cpp","c"];
    _aliases["Css"]=        ["css"];
    _aliases["Delphi"]=     ["delphi","pas","pascal"];
    _aliases["Diff"]=       ["diff","patch"];
    _aliases["Erlang"]=     ["erl","erlang"];
    _aliases["Groovy"]=     ["groovy"];
    _aliases["JScript"]=    ["js","jscript","javascript"];
    _aliases["Java"]=       ["java"];
    _aliases["JavaFX"]=     ["jfx","javafx"];
    _aliases["Perl"]=       ["perl","pl"];
    _aliases["Php"]=        ["php"];
    _aliases["Plain"]=      ["plain","text"];
    _aliases["PowerShell"]= ["ps","powershell"];
    _aliases["Python"]=     ["py","python"];
    _aliases["Ruby"]=       ["rails","ror","ruby"];
    _aliases["Scala"]=      ["scala"];
    _aliases["Sql"]=        ["sql"];
    _aliases["Vb"]=         ["vb","vbnet"];
    _aliases["Xml"] =        ["xml","xhtml","xslt","html","xhtml"];

    reBrushes = /brush\s?:\s?(\w+)/i;
    _blocks = [];
    //need brushes
    _brushes = [];
    //old style
    $('pre[name=code]').each(function(){
        this.className = "brush:" + this.className;
    });
    $('pre').each(function(){    
        if(reBrushes.test(this.className)){
            _blocks.push(RegExp.$1);
        }
    });

    for(i=0; i< _blocks.length; i++){
        for(key in _aliases){
        //相同brushes只载入一次
            if(jQuery.inArray(_blocks[i],_aliases[key]) >=0 && jQuery.inArray(key,_brushes) < 0){
                _brushes.push(key);
            }
        }
    }
    load_brushes = function(){
        for(k=0;k<_brushes.length;k++){
        //when last brush loaded, call hl()
                getScript(_media_root + '/js/sh/shBrush'+_brushes[k]+'.js',(k==_brushes.length -1)? hl:null);
            }    
    }
    if (_brushes.length >0){
        getStyles(_media_root + '/css/sh/shCore.css');
        getStyles(_media_root + '/css/sh/shThemeGitHub.css');
        getScript(_media_root + '/js/sh/shCore.js',load_brushes);
    }
}
$(document).ready(function(){
syntax_hl();
});