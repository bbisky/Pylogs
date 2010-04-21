tinyMCEPopup.requireLangPack();

var DFM = {
	init : function(ed) {
		tinyMCEPopup.resizeToInnerSize();
	},

	insert : function(file, title) {	
		var img = document.getElementById('prevImage');
		if (img)
		{
			var imgstr = '<img src="' + img.src + '" alt="img" />';
			tinyMCEPopup.restoreSelection();
			tinyMCE.execCommand("mceInsertContent", false, (imgstr));
			tinyMCEPopup.close();
		}
		
	},	
	resetImageData : function() {
		var f = document.forms[0];

		f.elements.width.value = f.elements.height.value = '';
	},

	updateImageData : function(img, st) {
		img.src = st;
	},
	prev : function(url){
		var div = document.getElementById('prev');
		if (div)
		{
			div.innerHTML = '';
			var img = document.createElement('img');
			img.id = 'prevImage';
			img.src = url;
			//img.onload = function(){DFM.updateImageData(this,url);};
			img.alt= '';
			div.appendChild(img);
		}
	}
};

tinyMCEPopup.onInit.add(DFM.init, DFM);