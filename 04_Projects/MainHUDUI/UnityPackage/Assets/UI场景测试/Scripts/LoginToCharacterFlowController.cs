using System.Collections;
using TMPro;
using UnityEngine;

namespace LargeLoginUI
{
    /// <summary>
    /// Test-scene flow: editable login form -> simulated successful login ->
    /// character/equipment selection screen -> transparent in-game HUD. A real
    /// account service can disable demo acceptance and call the Notify methods.
    /// </summary>
    [DisallowMultipleComponent]
    public sealed class LoginToCharacterFlowController : MonoBehaviour
    {
        [SerializeField] GameObject loginScreen;
        [SerializeField] GameObject characterScreen;
        [SerializeField] GameObject mainHudScreen;
        [SerializeField] LargeLoginScreenView loginView;
        [SerializeField] CanvasGroup loginCanvasGroup;
        [SerializeField] CanvasGroup characterCanvasGroup;
        [SerializeField] CanvasGroup mainHudCanvasGroup;
        [SerializeField] UnityEngine.UI.Button enterGameButton;
        [SerializeField] Material backgroundMaterial;
        [SerializeField] Texture loginBackground;
        [SerializeField] Texture characterBackground;
        [SerializeField] TMP_FontAsset cjkFontAsset;
        [SerializeField] bool acceptAnyNonEmptyCredentialsForDemo = true;
        [SerializeField, Min(0f)] float simulatedLoginDelay = 0.45f;
        [SerializeField, Min(0.01f)] float transitionDuration = 0.28f;

        TMP_FontAsset runtimeFont;
        Coroutine activeRoutine;
        bool subscribed;

        public void Configure(
            GameObject login,
            GameObject character,
            LargeLoginScreenView view,
            CanvasGroup loginGroup,
            CanvasGroup characterGroup,
            GameObject mainHud,
            CanvasGroup mainHudGroup,
            UnityEngine.UI.Button enterButton,
            Material backdropMaterial,
            Texture loginTexture,
            Texture characterTexture,
            TMP_FontAsset fontAsset)
        {
            loginScreen = login;
            characterScreen = character;
            loginView = view;
            loginCanvasGroup = loginGroup;
            characterCanvasGroup = characterGroup;
            mainHudScreen = mainHud;
            mainHudCanvasGroup = mainHudGroup;
            enterGameButton = enterButton;
            backgroundMaterial = backdropMaterial;
            loginBackground = loginTexture;
            characterBackground = characterTexture;
            cjkFontAsset = fontAsset;
        }

        void Awake()
        {
            ApplyCjkFont();
            ShowLoginImmediately();
        }

        void OnEnable()
        {
            Subscribe();
        }

        IEnumerator Start()
        {
            yield return null;
            if (loginView != null)
                loginView.FocusAccountInput();
        }

        void OnDisable()
        {
            Unsubscribe();
        }

        void OnDestroy()
        {
            if (runtimeFont != null)
                Destroy(runtimeFont);
        }

        void Subscribe()
        {
            if (subscribed || loginView == null)
                return;

            loginView.LoginRequested += HandleLoginRequested;
            loginView.RegisterRequested += HandleRegisterRequested;
            if (enterGameButton != null)
                enterGameButton.onClick.AddListener(HandleEnterGameRequested);
            subscribed = true;
        }

        void Unsubscribe()
        {
            if (!subscribed || loginView == null)
                return;

            loginView.LoginRequested -= HandleLoginRequested;
            loginView.RegisterRequested -= HandleRegisterRequested;
            if (enterGameButton != null)
                enterGameButton.onClick.RemoveListener(HandleEnterGameRequested);
            subscribed = false;
        }

        void HandleLoginRequested(string account, string password)
        {
            if (string.IsNullOrWhiteSpace(account) || string.IsNullOrWhiteSpace(password))
            {
                loginView.SetStatus("请先输入账号和密码", true);
                loginView.SetInteractable(true);
                return;
            }

            if (!acceptAnyNonEmptyCredentialsForDemo)
            {
                loginView.SetStatus("等待账号服务验证…");
                loginView.SetInteractable(false);
                return;
            }

            if (activeRoutine != null)
                StopCoroutine(activeRoutine);
            activeRoutine = StartCoroutine(SimulateSuccessfulLogin());
        }

        void HandleRegisterRequested()
        {
            if (loginView != null)
                loginView.SetStatus("测试场景尚未接入注册服务");
        }

        void HandleEnterGameRequested()
        {
            NotifyEnterGameSucceeded();
        }

        IEnumerator SimulateSuccessfulLogin()
        {
            loginView.SetInteractable(false);
            loginView.SetStatus("正在登录…");
            yield return new WaitForSecondsRealtime(simulatedLoginDelay);
            NotifyLoginSucceeded();
        }

        public void NotifyLoginSucceeded()
        {
            if (activeRoutine != null)
                StopCoroutine(activeRoutine);
            activeRoutine = StartCoroutine(TransitionToCharacter());
        }

        public void NotifyLoginFailed(string message)
        {
            if (activeRoutine != null)
            {
                StopCoroutine(activeRoutine);
                activeRoutine = null;
            }

            if (loginView == null)
                return;

            loginView.SetInteractable(true);
            loginView.SetStatus(
                string.IsNullOrWhiteSpace(message) ? "登录失败" : message,
                true);
        }

        public void NotifyEnterGameSucceeded()
        {
            if (activeRoutine != null)
                StopCoroutine(activeRoutine);
            activeRoutine = StartCoroutine(TransitionToMainHud());
        }

        IEnumerator TransitionToCharacter()
        {
            if (loginCanvasGroup == null || characterCanvasGroup == null)
                yield break;

            characterScreen.SetActive(true);
            characterCanvasGroup.alpha = 0f;
            characterCanvasGroup.interactable = false;
            characterCanvasGroup.blocksRaycasts = false;

            float elapsed = 0f;
            while (elapsed < transitionDuration)
            {
                elapsed += Time.unscaledDeltaTime;
                float t = Mathf.Clamp01(elapsed / transitionDuration);
                loginCanvasGroup.alpha = 1f - t;
                characterCanvasGroup.alpha = t;
                yield return null;
            }

            loginCanvasGroup.alpha = 0f;
            loginCanvasGroup.interactable = false;
            loginCanvasGroup.blocksRaycasts = false;
            loginScreen.SetActive(false);

            characterCanvasGroup.alpha = 1f;
            characterCanvasGroup.interactable = true;
            characterCanvasGroup.blocksRaycasts = true;
            ApplyBackground(characterBackground);
            activeRoutine = null;
        }

        IEnumerator TransitionToMainHud()
        {
            if (characterCanvasGroup == null || mainHudCanvasGroup == null ||
                characterScreen == null || mainHudScreen == null)
                yield break;

            mainHudScreen.SetActive(true);
            mainHudCanvasGroup.alpha = 0f;
            mainHudCanvasGroup.interactable = false;
            mainHudCanvasGroup.blocksRaycasts = false;

            float elapsed = 0f;
            while (elapsed < transitionDuration)
            {
                elapsed += Time.unscaledDeltaTime;
                float t = Mathf.Clamp01(elapsed / transitionDuration);
                characterCanvasGroup.alpha = 1f - t;
                mainHudCanvasGroup.alpha = t;
                yield return null;
            }

            characterCanvasGroup.alpha = 0f;
            characterCanvasGroup.interactable = false;
            characterCanvasGroup.blocksRaycasts = false;
            characterScreen.SetActive(false);

            mainHudCanvasGroup.alpha = 1f;
            mainHudCanvasGroup.interactable = true;
            mainHudCanvasGroup.blocksRaycasts = true;
            activeRoutine = null;
        }

        void ShowLoginImmediately()
        {
            if (loginScreen == null || characterScreen == null || mainHudScreen == null ||
                loginCanvasGroup == null || characterCanvasGroup == null ||
                mainHudCanvasGroup == null)
                return;

            loginScreen.SetActive(true);
            characterScreen.SetActive(false);
            mainHudScreen.SetActive(false);
            loginCanvasGroup.alpha = 1f;
            loginCanvasGroup.interactable = true;
            loginCanvasGroup.blocksRaycasts = true;
            characterCanvasGroup.alpha = 0f;
            characterCanvasGroup.interactable = false;
            characterCanvasGroup.blocksRaycasts = false;
            mainHudCanvasGroup.alpha = 0f;
            mainHudCanvasGroup.interactable = false;
            mainHudCanvasGroup.blocksRaycasts = false;
            ApplyBackground(loginBackground);

            if (loginView != null)
            {
                loginView.SetInteractable(true);
                loginView.SetStatus(string.Empty);
            }
        }

        void ApplyBackground(Texture texture)
        {
            if (backgroundMaterial == null || texture == null)
                return;

            backgroundMaterial.mainTexture = texture;
            if (backgroundMaterial.HasProperty("_BaseMap"))
                backgroundMaterial.SetTexture("_BaseMap", texture);
        }

        void ApplyCjkFont()
        {
            if (cjkFontAsset != null)
            {
                ApplyFontToHierarchy(loginScreen, cjkFontAsset);
                ApplyFontToHierarchy(characterScreen, cjkFontAsset);
                ApplyFontToHierarchy(mainHudScreen, cjkFontAsset);
                return;
            }

            Font osFont = Font.CreateDynamicFontFromOSFont(
                new[]
                {
                    "Microsoft YaHei UI",
                    "Microsoft YaHei",
                    "SimHei",
                    "PingFang SC",
                    "Noto Sans CJK SC",
                    "Arial Unicode MS"
                },
                32);

            if (osFont == null)
            {
                Debug.LogWarning("[LoginCharacterFlow] No system CJK font was found; retaining prefab fonts.");
                return;
            }

            runtimeFont = TMP_FontAsset.CreateFontAsset(osFont);
            if (runtimeFont == null)
            {
                Debug.LogWarning(
                    "[LoginCharacterFlow] System font was found but a TMP font asset " +
                    "could not be created; retaining prefab fonts.");
                return;
            }

            runtimeFont.name = "Runtime System CJK SDF";

            ApplyFontToHierarchy(loginScreen, runtimeFont);
            ApplyFontToHierarchy(characterScreen, runtimeFont);
            ApplyFontToHierarchy(mainHudScreen, runtimeFont);
        }

        static void ApplyFontToHierarchy(GameObject root, TMP_FontAsset fontAsset)
        {
            if (root == null || fontAsset == null)
                return;

            TMP_Text[] texts = root.GetComponentsInChildren<TMP_Text>(true);
            foreach (TMP_Text text in texts)
            {
                text.font = fontAsset;
                text.havePropertiesChanged = true;
            }
        }
    }
}
