$(function () {
    var navListItems = $('div.setup-panel div a'),
       allWells = $('.setup-content'),
       allNextBtn = $('.nextBtn');

    allWells.hide();
    navListItems.click(function (e) {
       e.preventDefault();
       var $target = $($(this).attr('href')),
          $item = $(this);

       if (!$item.hasClass('disabled')) {
          navListItems.removeClass('btn-primary').addClass('btn-default');
          $item.addClass('btn-primary');
          allWells.hide();
          $target.show();
          $target.find('input:eq(0)').focus();
       }
    });

    allNextBtn.click(function () {
       if ($(this).val()=="second"){
          var form = $( "#commentForm" ); 
          form.validate({
            rules: {
              phone: {
                required: true,
                digits:true,
                
              },
             
            } 
          });
       
          if (form.valid()) {
          var curStep = $(this).closest(".setup-content"),
          curStepBtn = curStep.attr("id"),
          nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
          curInputs = curStep.find("input[type='text'],input[type='url']"),
          isValid = true;
          }
          
        }
        else{
        var curStep = $(this).closest(".setup-content"),
        curStepBtn = curStep.attr("id"),
        nextStepWizard = $('div.setup-panel div a[href="#' + curStepBtn + '"]').parent().next().children("a"),
        curInputs = curStep.find("input[type='text'],input[type='url']"),
        isValid = true;

        }
       if (isValid)
          nextStepWizard.removeAttr('disabled').trigger('click');
    });

    $('div.setup-panel div a.btn-primary').trigger('click');
  
    $('.change_address_button').on('click', function () {
        $('.shipping-address-added').hide();
           if ($(this).prop('checked')) {
                 $('#showthis').fadeIn();
           } else {
                 $('#showthis').hide();
                 $('.shipping-address-added').show();
           }
        });
       
    
 });
 