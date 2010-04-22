(function() {
	tinymce.create('tinymce.plugins.FileManager', {
		init : function(ed, url) {
			var t = this;

			t.editor = ed;

			ed.addCommand('mceBrowseFile', function() {
				ed.windowManager.open({
					file : url + '/browser.htm',
					width : 580,
					height : 500,
					inline : 1
				}, {
					plugin_url : url
				});
			});

		
			ed.addButton('filemanager', {title : 'Django File manager', cmd : 'mceBrowseFile',image : url + '/img/icon.gif'});
		},

		getInfo : function() {
			return {
				longname : 'Django File Manager',
				author : 'Sky',
				authorurl : 'http://oteam.cn',
				infourl : 'http://oteam.cn/about',
				version : "0.1"
			};
		}
		
	});

	// Register plugin
	tinymce.PluginManager.add('filemanager', tinymce.plugins.FileManager);
})();