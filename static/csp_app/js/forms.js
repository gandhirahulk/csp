function CheckForOnlyNumbers(textbox, a) {
    if ((isNaN(textbox.value)) == true) {
        textbox.setCustomValidity('Please enter a valid ' + a + '!');
    } else {
        console.log('no isnan')
    }
    if (textbox.validity.typeMismatch) {
        textbox.setCustomValidity('Please enter a valid ' + a + '!');
    } else {
        textbox.setCustomValidity('');
    }

    return true;
}