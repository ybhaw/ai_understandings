"""
Good reads:
- https://www.pinecone.io/learn/series/faiss/hnsw/ : For understanding HNSW
- https://github.com/nmslib/hnswlib/ : A popular implementation of HNSW

I copied this logic from:
 https://github.com/nmslib/hnswlib/blob/master/hnswlib/hnswalg.h
"""

import logging


class HierarchicalNSW:
    MAX_LABEL_OPERATION_LOCKS = 65536
    DELETE_MARK = -1

    max_elements = 0
    current_element_count = 0
    size_data_per_element = 0
    size_links_per_element = 0

    num_deleted = 0
    M = 0
    max_M = 0
    max_M0 = 0
    ef_construction = 0
    ef = 0

    rev_size = 0.0
    max_level = 0

    visited_list_pool = 0

    label_op_locks = None

    global_ = None
    link_list_locks = None

    entry_point_node = None

    size_links_level_0 = 0
    offset_data = offset_level = label_offset = 0

    data_level_0_memory = None
    link_list = None
    element_levels = None

    data_size = 0

    fst_dist_func = None
    dist_func_param = None

    label_lookup_lock = None
    label_lookup = None

    level_generator = None
    update_probability_generator = None

    metric_distance_computations = 0
    metric_hops = 0

    allow_replace_delete = False

    delete_elements_lock = None
    delete_elements = None

    def apply_m(self, m):
        if m >= 10_000:
            logging.warning(
                "M parameter exceeds 10_000 which may lead to adverse effects. "
                "Cap to 10_000 will be applied for the rest of the processing."
            )
        self.M = min(m, 10_000)
        self.MAX_M = self.M
        self.EF_CONSTRUCTION = max(self.EF_CONSTRUCTION, self.M)
        self.EF = 10
