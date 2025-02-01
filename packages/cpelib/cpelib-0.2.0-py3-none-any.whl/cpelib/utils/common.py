XSD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

# Some common terms for reference tags are misspelled.
# CPU stands for Critical Patch Update, a security advisory published by Oracle.
REFERENCE_TAGS = {
    'Project': ['project'],
    'Version': ['version', 'versions', 'verisons', 'release', 'releases', 'archive', 'earlier'],
    'Advisory': ['advisory', 'advisories', 'vulnerability', 'vulnerabilities', 'security', 'report', 'bug', 'bugs',
                 'dsa', 'bsrt', 'apsb', 'aspsa', 'usn', 'cpu', 'dvisory'],
    'Vendor': ['vendor'],
    'Product': ['product', 'products', 'download', 'downloads', 'firmware', 'hardware', 'software', 'directory',
                'server'],
    'Changelog': ['changelog', 'change', 'log', 'changlog', 'changes'],
    'Website': ['website', 'page', 'search', 'site', 'sites', 'homepage', 'home', 'web', 'webpage', 'webpages'],
    'Update': ['bulletin', 'update', 'about', 'announcement', 'information', 'info', 'notice'],
    'Documentation': ['documentation', 'docs', 'manual', 'guide', 'support', 'faq'],
    'Community': ['community', 'forum', 'forums', 'mailing', 'list', 'lists', 'mailinglist', 'mailinglists'],
    'Specification': ['specification', 'specifications', 'spec', 'specs', 'standard', 'standards', 'datasheet',
                      'details'],
    'Mitigation': ['mitigation', 'mitigations', 'workaround', 'workarounds', 'patch', 'patches', 'fix', 'fixes',
                   'solution'],
    'Press/Media Coverage': ['article', 'articles', 'blog', 'blogs', 'post', 'posts', 'news', 'release', 'releases'],
    'Other': ['android', 'ios', 'itunes', 'apple', 'asus', 'google', 'models', 'cisco', 'ciscosa', 'cscug', 'citrix',
              'ctx', 'cobbler', 'condor', 'icsa', 'pkstat', 'axiom', 'txtman', 'latitude', 'password', 'proc', 'esa',
              'maintainer', 'reference', 'references', 'owner', 'source', 'sol', 'freebsd', 'fsc', 'developer',
              'developers', 'hpsbgn', 'hpsbhf', 'hpsbst', 'hpsbpi', 'rev.', 'hpsbmu', 'illumos', 'intel', 'mcafee',
              'ms']
}
