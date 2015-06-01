    ____________________').attr({ type: 'hidden', name: 'bn', value:
   'DragAndDropBuil_SP_EC' }).appendTo(product); } } }); }); } } else { //
   Prototype $$('div.blog-social div.fb-like').each(function(div) {
   div.className = 'blog-social-item blog-fb-like'; }); $$('#commentArea
   iframe').each(function(iframe) { iframe.style.minHeight = '410px'; });
   } } catch(ex) {} })(window._W && _W.jQuery);
