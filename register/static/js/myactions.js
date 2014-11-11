/* awesome code goes here */
(function($) {
    function hideif(elem, selector) {
	if (elem.value == "0") {
	    $(selector).hide();
	} else {
	    $(selector).show();
	}
    }
    
    $(document).ready(function() {
	hideif($('#id_kalenderstyrt')[0], 'div.field-periodicitet');
	hideif($('#id_beror_bransch')[0], 'div.field-bransch');
	hideif($('#id_beror_foretagsform')[0], 'div.field-foretagsform');


	$('#id_kalenderstyrt').change(function(){
	    hideif(this, 'div.field-periodicitet')});
	$('#id_beror_bransch').change(function(){
	    hideif(this, 'div.field-bransch')});
	$('#id_beror_foretagsform').change(function(){
	    hideif(this, 'div.field-foretagsform')});

	// # move inlines to their logical place in the form, see issue #15
	$('#blanketturl_set-group').appendTo($('div.field-blankett'));
	$('#etjansturl_set-group').appendTo($('div.field-etjanst'));
	
	// hide them if needed
	hideif($('#id_blankett')[0], '#blanketturl_set-group');
	hideif($('#id_etjanst')[0], '#etjansturl_set-group');
	$('#id_blankett').change(function(){
	    hideif(this, '#blanketturl_set-group')});
	$('#id_etjanst').change(function(){
	    hideif(this, '#etjansturl_set-group')});


    })
})(django.jQuery);


