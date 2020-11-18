function showForm(designation) {

    var login_options = document.getElementById('login-options');
    var form = document.getElementById(designation);

    login_options.style.display = 'none';
    form.style.display = 'block';

};

function showJobForm(designation) {

    var job_options = document.getElementById('job-options');
    var form = document.getElementById(designation);

    job_options.style.display = 'none';
    form.style.display = 'block';

};

function hideForm(designation) {

    var login_options = document.getElementById('login-options');
    var form = document.getElementById(designation);

    login_options.style.display = 'block';
    form.style.display = 'none';
};

function hideJobForm(designation) {

    var job_options = document.getElementById('job-options');
    var form = document.getElementById(designation);

    job_options.style.display = 'block';
    form.style.display = 'none';
};

function goback() {
    window.history.back();
};

function dismissFlash(messageID) {
    var message = document.getElementById(messageID);
    message.style.display = 'none';
};

function showLoginForms() {

    var Condition = document.getElementById('form-show').innerHTML;

    if (Condition == 'reader') {
        showForm('Reader_login');
    } else if (Condition == 'author') {
        showForm('Author_login');
    } else if (Condition == 'authority') {
        showForm('Authority_login');
    };

};

function guestLogin() {
    document.getElementById('guest-login-btn').click();
};

function showAuthForm() {

    var Condition = document.getElementById('form-show').innerHTML;

    if (Condition == 'show') {
        document.getElementById('authority-signup-code').style.display = 'none';
        document.getElementById('signup-form').style.display = 'block';
    };

};