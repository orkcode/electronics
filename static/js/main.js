document.addEventListener('htmx:configRequest', function(event) {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});

document.body.addEventListener('htmx:beforeSwap', function(event) {
    const target = event.detail.target;
    if (target.closest('.modal')) {
        const modal = new bootstrap.Modal(target.closest('.modal'));
        modal.show();
    }
});

document.body.addEventListener('htmx:swapSuccess', function(event) {
    const response = event.detail.response;
    if (response.rendered_form) {
        const target = event.detail.target;
        target.outerHTML = response.rendered_form;
    }
});