(function() {
	$(document).ready(function() {
	$('#element_to_pop_up').bPopup();
    var cells, count, likeClickCallback, loadCheck, loadImage, loadLock, offset;
    offset = 1;
    count = 17;
    cells = $('#content');
    loadLock = false;
    loadCheck = function() {
      	var height, top;
      	height = window.innerHeight || document.documentElement.clientHeight;
      	top = document.documentElement.scrollTop || document.body.scrollTop;
      	if (height + top > cells.height() && !loadLock) {
        	loadLock = true;
        	return true;
      	} else {
        	return false;
      	}
    };
    likeClickCallback = function(e) {
    var imgId;
    imgId = e.currentTarget.id.split('-')[1];
    return $.post("../like/" + imgId.split('.')[0] + "/", null, function(data) {
        var countElem;
        countElem = e.currentTarget.parentElement.parentElement.parentElement.children[0];
        return countElem.innerHTML = "" + countElem.innerHTML.slice(0, 2) + data;
      }, 'json');
    };
    loadImage = function() {
		alert(offset);
      return $.get('../getImage/', {
        offset: offset,
        count: count
      }, function(data) {
        var callback, cell, i, img, len_p, pos, timeoffset, _len;
        timeoffset = 10;
        for (i = 0, _len = data.length; i < _len; i++) {
          img = data[i];
          if (img.orig_width > img.orig_height) {
          		len_p = 'height';
            pos = "left: -" + (parseInt((img.orig_width * 237 / img.orig_height - 237) / 2)) + "px;";
          } else {
            len_p = 'width';
            pos = "top: -" + (parseInt((img.orig_height * 237 / img.orig_width - 237) / 2)) + "px;";
          }
          cell = document.createElement('div');
          cell.className = 'cell';
          cell.innerHTML = "<div class=\"tip\">\n  <small>❤×" + img.liked_count + "</small>\n  <p><small>\n    <a class=\"like\" id=\"image-" + img.id + "\" href=\"javascript:void(0);\">飘过</a> </small></p>\n</div>\n <a>\n  <img " + len_p + "=\"237px\" src=\"/images/img/"  + img.id  + "\"\n    style=\"position: relative; " + pos + "\" />\n</a>";
          cells.append(cell);
          callback = function(c) {
            return function() {
              return c.className = 'cell ready';
            };
          };
          setTimeout(callback(cell), 100 * i + 1);
          loadLock = false;
        }
        offset += data.length;
        $('.like').unbind('click');
        return $('.like').click(likeClickCallback);
      }, "json");
    };
    $(window).scroll(function() {
      if (loadCheck()) return loadImage();
    });
    return loadImage();
  });

}).call(this);
