export const validateRequired = (value) => {
    return !!value || "This field is required.";
};

export const validateEmail = (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value) || "Invalid email address.";
};

export const validatePassword = (value) => {
    if (value.length < 8 || value.length > 128)
        return "Password must be between 8 and 128 characters.";
    if (!/\d/.test(value) || !/[A-Za-z]/.test(value))
        return "Password must contain at least one letter and one number.";
    return true;
};

export const validateField = (value, validators) => {
    for (const validator of validators) {
        const result = validator(value);
        if (result !== true) return result; // Return the first error message
    }
    return ''; // All validators passed
};