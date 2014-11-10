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
    })
})(django.jQuery);


