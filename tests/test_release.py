import importlib.util, tempfile, unittest
from pathlib import Path
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('course_builder',ROOT/'scripts/build_site.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
class Links(HTMLParser):
    def __init__(self,text):super().__init__();self.ids=set();self.links=[];self.feed(text)
    def handle_starttag(self,t,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ('href','src'):
            if k in a:self.links.append(a[k])
class ReleaseTests(unittest.TestCase):
    def output(self,when):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup)
        dest=(Path(temp.name)/'site').resolve();builder.build(dest,datetime.fromisoformat(when));return dest
    def assert_links(self,dest):
        for page in dest.rglob('*.html'):
            for link in Links(page.read_text()).links:
                u=urlsplit(link)
                if u.scheme or u.netloc:continue
                target=(page.parent/unquote(u.path)).resolve() if u.path else page
                self.assertTrue(target.is_file(),f'{page.name}: {link}')
                self.assertTrue(target.is_relative_to(dest))
                if u.fragment:self.assertIn(u.fragment,Links(target.read_text()).ids)
    def test_before_release_excludes_all_materials_and_question_bodies(self):
        dest=self.output('2026-10-04T23:59:59+08:00')
        self.assertEqual(list(dest.rglob('*.zip')),[])
        self.assertEqual(list(dest.rglob('*.pptx')),[])
        self.assertEqual(list(dest.rglob('*.txt')),[])
        self.assertFalse((dest/'content').exists())
        for n in range(1,7):
            page=(dest/f'projects/project{n}/index.html').read_text()
            self.assertIn('未开放',page);self.assertNotIn('INSERT INTO',page)
            self.assertEqual(len(list((dest/f'projects/project{n}').iterdir())),1)
        self.assert_links(dest)
    def test_opens_at_exact_beijing_boundary(self):
        dest=self.output('2026-10-04T16:00:00+00:00')
        self.assertTrue((dest/'projects/project1/materials/project1_data.zip').is_file())
        self.assertIn('INSERT INTO',(dest/'projects/project1/index.html').read_text())
        for n in range(2,7):self.assertFalse((dest/f'projects/project{n}/materials').exists())
        self.assert_links(dest)
    def test_deadline_does_not_relock_learning_materials(self):
        dest=self.output('2026-10-19T00:00:00+08:00')
        self.assertIn('提交已截止',(dest/'index.html').read_text())
        self.assertTrue((dest/'projects/project1/data/student.txt').is_file())
    def test_undated_projects_remain_locked_in_future(self):
        dest=self.output('2030-01-01T00:00:00+08:00')
        for n in range(2,7):self.assertEqual(len(list((dest/f'projects/project{n}').iterdir())),1)
    @unittest.skipUnless((ROOT/'content/project2.html').exists(), 'Unreleased project sources are local only')
    def test_all_future_project_downloads_resolve(self):
        import json
        from unittest.mock import patch
        config=json.loads((ROOT/'config/course.json').read_text())
        for project in config['projects']:project['release_at']='2026-10-05T00:00:00+08:00'
        with patch.object(builder.json,'loads',return_value=config):
            dest=self.output('2026-10-05T00:00:00+08:00')
        self.assert_links(dest)
        for n in range(1,7):self.assertTrue((dest/f'projects/project{n}/materials').is_dir())
    def test_timezone_required(self):
        with self.assertRaises(ValueError):builder.parse_time('2026-10-05T00:00:00')
        with self.assertRaises(ValueError):builder.is_released({'release_at':'2026-10-05T00:00:00+08:00'},datetime(2026,10,5))
    def test_source_assets_are_intact(self):
        import json,hashlib
        for item in json.loads((ROOT/'config/assets.json').read_text()):
            self.assertEqual(hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest(),item['sha256'])
        local_manifest=ROOT/'content/manifest.json'
        if local_manifest.exists():
            for item in json.loads(local_manifest.read_text()):
                self.assertEqual(hashlib.sha256((ROOT/'content'/item['path']).read_bytes()).hexdigest(),item['sha256'])
if __name__=='__main__':unittest.main()
