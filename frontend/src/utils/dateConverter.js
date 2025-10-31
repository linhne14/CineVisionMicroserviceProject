const dateConvert = (date) => {
    return new Date(date).toLocaleDateString("vi-VN", {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

export default dateConvert;