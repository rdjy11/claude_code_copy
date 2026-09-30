# -*- coding: utf-8 -*-
"""build_domain_index 归类核心的单元测试（标准库 unittest）"""
import os
import sys
import unittest

# 保证能直接 import 同目录下的被测模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from build_domain_index import (
    EXPERT_KEYWORDS, EXPERT_TITLES, META_KEYWORDS,
    classify, is_meta, volume_of,
)


class TestClassify(unittest.TestCase):
    def test_word_boundary_rejects_substring(self):
        """词边界：'can' 不得命中 cannot / candidate（Review Focus #5 的姊妹问题）"""
        self.assertNotIn("bt-can-lin-flexray", classify("Cannot connect", "candidate node"))
        self.assertIn("bt-can-lin-flexray", classify("CAN bus speed", "the can bus shall"))

    def test_multi_label(self):
        """一条需求可同时命中多个域"""
        got = classify("Bootloader DTC handling", "the flash sequence shall set a DTC")
        self.assertIn("bt-flash", got)
        self.assertIn("bt-dtc", got)

    def test_unassigned_returns_empty_list(self):
        """无任何关键词命中时返回空列表，而非 None"""
        self.assertEqual(classify("Document precedence", "priority between documents"), [])

    def test_returns_expert_names_only(self):
        """返回值必须是 EXPERT_KEYWORDS 的键，且按该字典的键顺序"""
        got = classify("CAN bus and UDS session", "diagnostic session shall")
        self.assertTrue(set(got) <= set(EXPERT_KEYWORDS))
        order = [k for k in EXPERT_KEYWORDS if k in got]
        self.assertEqual(got, order)

    def test_weak_keyword_counts_in_title_only(self):
        """
        泛化词（frame / power / wire / period 等）只在标题里算数。
        正文动辄上千字符，泛词在正文里出现的概率极高，若一并计入会把
        大量无关需求卷进域索引（实测 bt-can-lin-flexray 有 48% 属此类）。
        """
        # 标题无信号、正文含泛词 → 不应归入
        self.assertNotIn("bt-can-lin-flexray", classify("DTC setting", "the frame shall be sent"))
        self.assertNotIn("bt-platform", classify("DTC setting", "supply the power wire pin"))
        # 标题含泛词 → 应归入
        self.assertIn("bt-can-lin-flexray", classify("Frame format", "shall be sent"))

    def test_weak_keyword_plurals_also_title_only(self):
        """
        泛化词的复数形式必须与单数同规则（只在标题里算数）。
        实测遗漏：frame/header 已入 WEAK_KEYWORDS，但 frames/headers 未入，
        仍按强词在正文匹配——与「泛化词仅标题」的设计自相矛盾。
        """
        self.assertNotIn("bt-can-lin-flexray", classify("DTC setting", "the frames shall be sent"))
        self.assertNotIn("bt-can-lin-flexray", classify("DTC setting", "the headers shall be sent"))

    def test_compound_term_separator_variants(self):
        """
        复合词的分隔变体应等价命中。
        实测缺陷：需求 2362《ECU start up time》只进了 bt-nm 索引、没进 bt-platform，
        因为关键词只收了连写形式 `startup time`，漏了 `start up` / `start-up`。
        """
        for title in ("Startup Time", "ECU start up time", "ECU start-up time"):
            self.assertIn("bt-platform", classify(title, "shall start quickly"),
                          f"未命中平台域：{title}")


class TestIsMeta(unittest.TestCase):
    def test_meta_rule_detected(self):
        self.assertTrue(is_meta("Document precedence", "priority between standard documents"))

    def test_technical_req_not_meta(self):
        self.assertFalse(is_meta("DTC setting", "the ECU shall set a DTC"))


class TestVolumeOf(unittest.TestCase):
    def test_boundaries(self):
        """卷边界必须精确落在 filenames 标注的区间上"""
        self.assertEqual(volume_of(355), "01_355-491")
        self.assertEqual(volume_of(491), "01_355-491")
        self.assertEqual(volume_of(492), "02_492-1128")
        self.assertEqual(volume_of(6724), "20_3533-6724")


def _read(path):
    """读文件并确保关闭（避免 ResourceWarning 污染测试输出）"""
    with open(path, encoding="utf-8") as f:
        return f.read()


class TestBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import tempfile
        import build_domain_index as B
        cls.B = B
        cls.tmp = tempfile.mkdtemp()
        cls.stats = B.build(cls.tmp, B.JSON_PATH)

    def test_eleven_indexes_and_meta_written(self):
        """必须产出 11 份域索引 + 1 份 meta-rules.md"""
        d = os.path.join(self.tmp, "_index", "by-domain")
        names = sorted(os.listdir(d))
        self.assertEqual(len(names), 11)
        self.assertEqual(names, sorted(f"{k}.md" for k in self.B.EXPERT_KEYWORDS))
        self.assertTrue(os.path.exists(os.path.join(self.tmp, "_index", "meta-rules.md")))

    def test_zero_blindspot(self):
        """零无处置盲区：未命中且非元规则的条目必须为 0"""
        self.assertEqual(self.stats["unassigned"], [],
                         f"仍有未命中需求：{self.stats['unassigned'][:10]}")

    def test_index_cross_consistency(self):
        """Review Focus #5：同一编号在多份索引中的标题必须逐字相同"""
        import re
        d = os.path.join(self.tmp, "_index", "by-domain")
        seen = {}
        for fn in os.listdir(d):
            text = _read(os.path.join(d, fn))
            for m in re.finditer(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|", text, re.M):
                rid, title = int(m.group(1)), m.group(2)
                if rid in seen:
                    self.assertEqual(seen[rid], title, f"编号 {rid} 标题不一致")
                seen[rid] = title

    def test_index_volume_column_matches_corpus_files(self):
        """索引中的语料卷短名必须真实存在于 Basetech知识库语料/"""
        import re
        import glob
        corpus = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(self.B.__file__))), "Basetech知识库语料")
        real = {re.match(r"SWRS_DHU_语料_(\d+_\d+-\d+)\.md", os.path.basename(p)).group(1)
                for p in glob.glob(os.path.join(corpus, "SWRS_DHU_语料_*.md"))}
        d = os.path.join(self.tmp, "_index", "by-domain")
        for fn in os.listdir(d):
            text = _read(os.path.join(d, fn))
            for m in re.finditer(r"^\|\s*\d+\s*\|.+?\|\s*(\d+_\d+-\d+)\s*\|", text, re.M):
                self.assertIn(m.group(1), real)


if __name__ == "__main__":
    unittest.main()
