"""核心函数单元测试"""
import sys, os, unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestComponentDedup(unittest.TestCase):
    """测试 component-dedup.py 的核心函数"""

    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'dedup', 'scripts/component-dedup.py')
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_normalize_basic(self):
        self.assertEqual(self.mod.normalize('Button'), 'button')
        self.assertEqual(self.mod.normalize('  Search Box  '), 'search box')

    def test_normalize_special_chars(self):
        self.assertEqual(self.mod.normalize('ic_small'), 'ic small')
        self.assertEqual(self.mod.normalize('loader-wheel'), 'loader wheel')
        self.assertEqual(self.mod.normalize('icon.home'), 'icon home')


class TestRefineClassificationV2(unittest.TestCase):
    """测试 refine-classification.py 的增强分类函数"""

    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'refine', 'scripts/refine-classification.py')
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_classify_button(self):
        self.assertEqual(self.mod.classify_v2('Button'), 'button')
        self.assertEqual(self.mod.classify_v2('Primary Btn'), 'button')
        self.assertEqual(self.mod.classify_v2('CTA Large'), 'button')

    def test_classify_icon(self):
        self.assertEqual(self.mod.classify_v2('icon.home'), 'icon')
        self.assertEqual(self.mod.classify_v2('ic_arrow'), 'icon')

    def test_classify_toggle(self):
        self.assertEqual(self.mod.classify_v2('Checkbox'), 'toggle')
        self.assertEqual(self.mod.classify_v2('Radio'), 'toggle')
        self.assertEqual(self.mod.classify_v2('Switch'), 'toggle')

    def test_classify_modal(self):
        self.assertEqual(self.mod.classify_v2('Bottom Sheet'), 'modal')
        self.assertEqual(self.mod.classify_v2('popup dialog'), 'modal')
        self.assertEqual(self.mod.classify_v2('Action Sheet'), 'modal')

    def test_classify_payment_flow(self):
        self.assertEqual(
            self.mod.classify_v2('Payment Summary', 'checkout'), 'payment-flow')
        self.assertEqual(
            self.mod.classify_v2('Top Up Amount'), 'payment-flow')

    def test_classify_kyc_flow(self):
        self.assertEqual(self.mod.classify_v2('KYC/sub.Selfie'), 'kyc-flow')
        self.assertEqual(
            self.mod.classify_v2('Liveness Check'), 'kyc-flow')

    def test_classify_gesture(self):
        self.assertEqual(self.mod.classify_v2('Hand Gesture 1'), 'gesture')
        self.assertEqual(
            self.mod.classify_v2('TwoFinger Swipe'), 'gesture')

    def test_classify_uncategorized(self):
        self.assertEqual(
            self.mod.classify_v2('XYZ Random Name'), 'uncategorized')

    def test_classify_screen(self):
        self.assertEqual(
            self.mod.classify_v2('Transaction/sub.Details'), 'screen')

    def test_classify_onboarding_takes_priority(self):
        """Onboarding 优先于通用 screen 分类"""
        self.assertEqual(
            self.mod.classify_v2('Onboarding/sub.Step1'), 'onboarding')

    def test_classify_error_state(self):
        self.assertEqual(
            self.mod.classify_v2('Empty State No Results'), 'error-state')
        self.assertEqual(
            self.mod.classify_v2("Can't connect right now"), 'error-state')


class TestRefineClassification(unittest.TestCase):
    """测试 refine-classification.py 的分类函数"""

    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'refine', 'scripts/refine-classification.py')
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_detect_platform_mobile(self):
        self.assertEqual(
            self.mod.detect_platform('Design library - Mobile'), 'mobile')
        self.assertEqual(
            self.mod.detect_platform('[Content] Mobile'), 'mobile')

    def test_detect_platform_web(self):
        self.assertEqual(
            self.mod.detect_platform('[Design System] Web'), 'web')
        self.assertEqual(
            self.mod.detect_platform('Screen library - web'), 'web')

    def test_detect_platform_shared(self):
        self.assertEqual(
            self.mod.detect_platform('Icon Library'), 'shared')
        self.assertEqual(
            self.mod.detect_platform('[Asset] Illustration'), 'shared')

    def test_detect_platform_unknown(self):
        self.assertEqual(
            self.mod.detect_platform('Flow Library'), 'unknown')


class TestW3CExport(unittest.TestCase):
    """测试 W3C Token 导出的辅助函数"""

    def setUp(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'w3c', 'scripts/export-w3c-tokens.py')
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def test_hex_to_srgb_full_opacity(self):
        self.assertEqual(self.mod.hex_to_srgb('#FF0000', 1.0), '#ff0000')

    def test_hex_to_srgb_partial_opacity(self):
        result = self.mod.hex_to_srgb('#FF0000', 0.5)
        self.assertEqual(result, '#ff00007f')

    def test_normalize_name_basic(self):
        self.assertEqual(
            self.mod.normalize_name('Button/Default'), 'button.default')

    def test_normalize_name_with_hex(self):
        self.assertEqual(
            self.mod.normalize_name('greyscale/dark 1 #141C30'),
            'greyscale.dark-1')

    def test_normalize_name_spaces(self):
        self.assertEqual(
            self.mod.normalize_name('Body Bold/Large'),
            'body-bold.large')


if __name__ == '__main__':
    unittest.main(verbosity=2)
