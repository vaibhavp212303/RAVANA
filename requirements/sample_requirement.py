requirement = {
    "loginPage": {
        "application": "Scoreboard",
        "powered_by": "Clippd",
        "flow": "Sign in",
        "steps": [
            {
                "step": 1,
                "title": "Sign in to Scoreboard",
                "subtitle": "Welcome back! Please sign in to continue",
                "options": {
                    "social_login": [
                        {
                            "provider": "Apple",
                            "action": "sign_in_with_apple"
                        },
                        {
                            "provider": "Facebook",
                            "action": "sign_in_with_facebook"
                        },
                        {
                            "provider": "Google",
                            "action": "sign_in_with_google"
                        }
                    ],
                    "email_login": {
                        "field": {
                            "type": "text",
                            "label": "Email address",
                            "placeholder": "Enter your email address",
                            "required": True
                        },
                        "button": {
                            "text": "Continue",
                            "action": "go_to_password_step"
                        }
                    }
                },
                "footer": {
                    "signup_prompt": "Don't have an account?",
                    "signup_link": "Sign up",
                    "help_link": "Help",
                    "dev_mode_label": "Development mode"
                }
            },
            {
                "step": 2,
                "title": "Enter your password",
                "subtitle": "Enter the password associated with your account",
                "account": "vaibhav.pawar+sb78@clippd.io",
                "fields": {
                    "password": {
                        "type": "password",
                        "label": "Password",
                        "required": True,
                        "actions": {
                            "forgot_password_link": "Forgot password?",
                            "show_hide_toggle": True
                        }
                    }
                },
                "button": {
                    "text": "Continue",
                    "action": "authenticate_user"
                },
                "alternatives": {
                    "use_another_method": {
                        "action": "go_to_alternate_methods"
                    }
                },
                "footer": {
                    "help_link": "Help",
                    "dev_mode_label": "Development mode"
                }
            },
            {
                "step": 3,
                "title": "Use another method",
                "subtitle": "Facing issues? You can use any of these methods to sign in.",
                "options": {
                    "social_login": [
                        {
                            "provider": "Apple",
                            "action": "sign_in_with_apple"
                        },
                        {
                            "provider": "Facebook",
                            "action": "sign_in_with_facebook"
                        },
                        {
                            "provider": "Google",
                            "action": "sign_in_with_google"
                        }
                    ],
                    "email_otp": {
                        "action": "send_email_code",
                        "label": "Email code to vaibhav.pawar+sb78@clippd.io"
                    }
                },
                "button": {
                    "text": "Back",
                    "action": "return_to_password_step"
                },
                "footer": {
                    "help_link": "Help",
                    "get_help_text": "Don't have any of these? Get help",
                    "dev_mode_label": "Development mode"
                }
            }
        ]
    }
}