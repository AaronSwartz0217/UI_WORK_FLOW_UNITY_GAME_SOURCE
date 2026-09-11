using System;
using TMPro;
using UnityEngine;
using UnityEngine.Events;
using UnityEngine.UI;

namespace LargeLoginUI
{
    /// <summary>
    /// Presentation-only controller for the generated login prefab.
    /// Authentication and scene switching intentionally remain in the host game.
    /// </summary>
    public sealed class LargeLoginScreenView : MonoBehaviour
    {
        [SerializeField] TMP_InputField accountInput;
        [SerializeField] TMP_InputField passwordInput;
        [SerializeField] Button loginButton;
        [SerializeField] Button registerButton;
        [SerializeField] TMP_Text statusLabel;

        public event Action<string, string> LoginRequested;
        public event Action RegisterRequested;

        public string Account => accountInput != null ? accountInput.text : string.Empty;
        public string Password => passwordInput != null ? passwordInput.text : string.Empty;

        public void Configure(
            TMP_InputField account,
            TMP_InputField password,
            Button login,
            Button register,
            TMP_Text status)
        {
            accountInput = account;
            passwordInput = password;
            loginButton = login;
            registerButton = register;
            statusLabel = status;
        }

        void OnEnable()
        {
            AddListeners();
        }

        void OnDisable()
        {
            RemoveListeners();
        }

        void AddListeners()
        {
            if (loginButton != null)
                loginButton.onClick.AddListener(OnLoginClicked);
            if (registerButton != null)
                registerButton.onClick.AddListener(OnRegisterClicked);
        }

        void RemoveListeners()
        {
            if (loginButton != null)
                loginButton.onClick.RemoveListener(OnLoginClicked);
            if (registerButton != null)
                registerButton.onClick.RemoveListener(OnRegisterClicked);
        }

        void OnLoginClicked()
        {
            LoginRequested?.Invoke(Account, Password);
        }

        void OnRegisterClicked()
        {
            RegisterRequested?.Invoke();
        }

        public void SetStatus(string message, bool isError = false)
        {
            if (statusLabel == null)
                return;

            statusLabel.text = message ?? string.Empty;
            statusLabel.color = isError
                ? new Color(1f, 0.29f, 0.19f, 1f)
                : new Color(1f, 0.82f, 0.49f, 1f);
            statusLabel.gameObject.SetActive(!string.IsNullOrWhiteSpace(message));
        }

        public void SetInteractable(bool interactable)
        {
            if (accountInput != null)
                accountInput.interactable = interactable;
            if (passwordInput != null)
                passwordInput.interactable = interactable;
            if (loginButton != null)
                loginButton.interactable = interactable;
            if (registerButton != null)
                registerButton.interactable = interactable;
        }
    }
}
