var GP = GP || {};

var Validator = (function() {
  var $trackButton = $('#track-button');

  function addTrackButtonClickListener() {
    $trackButton.click(handleTrackBtnClick);
  }

  function handleTrackBtnClick(event) {
    event.preventDefault();
    validateFormInput();
  }

  function validateFormInput() {
    var $formInput = $('#tracking-number-input').val().toUpperCase().trim();
    var emptyError = 'Please enter a tracking number.';
    var formatError = 'Please enter a valid UPS tracking number. Ex: 1ZY8Y608YW02920325';
    var duplicateError = 'You are already tracking that number.'
    var errorMessage = false;
    
    $('#error-message').empty();

    if ($formInput === '') {
      errorMessage = emptyError;
    } else if (!/1Z[A-Z0-9]{16}/.test($formInput)) {
      errorMessage = formatError;
    } else {
      $('.tracking-number-td').each(function() {
        if ($(this).text() === $formInput) {
          errorMessage = duplicateError;
          // break out of the loop early
          return false;
        }
      });
    }

    if (errorMessage) {
      $('#error-message').html(errorMessage).removeClass('hidden');
    } else {
      $('#error-message').addClass('hidden');
      $('#add-form').submit();
    }
  }

  function init() {
    addTrackButtonClickListener();
  }

  return {
    init: init
  };
})();

$(document).ready(function () {
  GP.validator = Validator.init();
});
