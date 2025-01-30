INITIALIZE_TEMPLATE = """
const express = require('express');
const app = express();
app.use(express.json());
"""

GET_TEMPLATE = """
{{ anchor_get_main_begin }}
app.get('/{{ route }}', (req, res) => {
    res.json({"message": "GET {{ route }} called"});
});
"""

POST_TEMPLATE = """
{{ anchor_post_main_begin }}
app.post('/{{ route }}', (req, res) => {
    res.json({"message": "POST {{ route }} called"});
});
"""

PUT_TEMPLATE = """
{{ anchor_put_main_begin }}
app.put('/{{ route }}', (req, res) => {
    res.json({"message": "PUT {{ route }} called"});
});
"""

PATCH_TEMPLATE = """
{{ anchor_patch_main_begin }}
app.patch('/{{ route }}', (req, res) => {
    res.json({"message": "PATCH {{ route }} called"});
});
"""

DELETE_TEMPLATE = """
{{ anchor_delete_main_begin }}
app.delete('/{{ route }}', (req, res) => {
    res.json({"message": "DELETE {{ route }} called"});
});
"""

FINALIZE_TEMPLATE = """
{{ anchor_finalize_begin }}
const PORT = {{ port }};
app.listen(PORT, () => {
    console.log(`Server running on http://{{ host }}:${PORT}`);
});
"""
