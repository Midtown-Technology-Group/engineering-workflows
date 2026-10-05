from pathlib import Path
import re
import unittest
import yaml

class WorkflowTests(unittest.TestCase):
    def test_scan_security_contract(self):
        text = Path('.github/workflows/sonar.yml').read_text()
        data = yaml.safe_load(text)
        self.assertEqual(data['permissions'], {'contents': 'read'})
        self.assertIn('head.repo.full_name == github.repository', data['jobs']['scan']['if'])
        self.assertIn('github.event.repository.default_branch', data['jobs']['scan']['if'])
        self.assertIn("github.event_name == 'pull_request'", data['jobs']['scan']['if'])
        self.assertNotIn('pull_request_target', text)
        self.assertNotIn('secrets: inherit', text)
        for step in data['jobs']['scan']['steps']:
            if 'uses' in step: self.assertRegex(step['uses'], r'@[0-9a-f]{40}$')
        self.assertIn('sonar.scm.revision', text)
        self.assertIn('sonar.qualitygate.timeout=300', text)
        self.assertIn('.scannerwork/report-task.txt', text)
