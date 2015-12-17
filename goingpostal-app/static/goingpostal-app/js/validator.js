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
    var $formInput = $('#tracking-number-input').val().trim();
    var emptyError = 'Please enter a tracking number.';
    var invalidTrackingNumber = 'Please enter a valid UPS tracking number. Ex: 1ZY8Y608YW02920325';
    var errorMessage = false;
    
    $('#error-message').empty();

    if ($formInput === '') {
      errorMessage = emptyError;
    } else if (!/1Z[A-Z0-9]{16}/.test($formInput)) {
      errorMessage = invalidTrackingNumber;
    }

    if (errorMessage) {
      $('#error-message').html(errorMessage).removeClass('hidden');
    } else {
      $('#error-message').addClass('hidden');
      location.assign('/track?tn=' + $formInput);
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
