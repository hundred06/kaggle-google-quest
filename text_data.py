import numpy as np
from torch.utils.data import Dataset

from common import N_TARGETS


class TextDataset(Dataset):

    def __init__(self, question_data, answer_data, title_data, category_data, 
                 host_data, use_embeddings, dist_features, idxs, targets=None):
        self.question_data = question_data[idxs].astype(np.long)
        self.answer_data = answer_data[idxs].astype(np.long)
        self.title_data = title_data[idxs].astype(np.long)
        self.category_data = category_data[idxs].astype(np.long)
        self.host_data = host_data[idxs].astype(np.long)
        self.use_embeddings_q = use_embeddings['question_body_embedding'][idxs].astype(np.float32)
        self.use_embeddings_a = use_embeddings['answer_embedding'][idxs].astype(np.float32)
        self.use_embeddings_t = use_embeddings['question_title_embedding'][idxs].astype(np.float32)
        self.dist_features = dist_features[idxs].astype(np.float32)
        if targets is not None: self.targets = targets[idxs].astype(np.float32)
        else: self.targets = np.zeros((self.question_data.shape[0], N_TARGETS), dtype=np.float32)

    def __getitem__(self, idx):
        question = self.question_data[idx]
        answer = self.answer_data[idx]
        title = self.title_data[idx]
        category = self.category_data[idx]
        host = self.host_data[idx]
        use_emb_q = self.use_embeddings_q[idx]
        use_emb_a = self.use_embeddings_a[idx]
        use_emb_t = self.use_embeddings_t[idx]
        dist_feature = self.dist_features[idx]
        target = self.targets[idx]

        return (question, answer, title, category, host, use_emb_q, use_emb_a, 
                use_emb_t, dist_feature), target

    def __len__(self):
        return len(self.question_data)

class TextDataset2(Dataset):

    def __init__(self, x_features, x_question_emb, x_answer_emb, x_title_emb, 
                 question_ids, answer_ids, title_ids, idxs, targets=None):
        self.question_ids = question_ids[idxs].astype(np.long)
        self.answer_ids = answer_ids[idxs].astype(np.long)
        self.title_ids = title_ids[idxs].astype(np.long)
        self.x_question_emb = x_question_emb[idxs].astype(np.float32)
        self.x_answer_emb = x_answer_emb[idxs].astype(np.float32)
        self.x_title_emb = x_title_emb[idxs].astype(np.float32)
        self.x_features = x_features[idxs].astype(np.float32)
        if targets is not None: self.targets = targets[idxs].astype(np.float32)
        else: self.targets = np.zeros((self.x_question_emb.shape[0], N_TARGETS), dtype=np.float32)

    def __getitem__(self, idx):
        q_ids = self.question_ids[idx]
        a_ids = self.answer_ids[idx]
        # t_ids = self.title_ids[idx]
        q_att_mask = np.where(q_ids != 0, 1, 0)
        a_att_mask = np.where(a_ids != 0, 1, 0)
        # t_att_mask = np.where(t_ids != 0, 1, 0)
        x_q_emb = self.x_question_emb[idx]
        x_a_emb = self.x_answer_emb[idx]
        x_t_emb = self.x_title_emb[idx]
        x_feats = self.x_features[idx]
        target = self.targets[idx]
        return (x_feats, x_q_emb, x_t_emb, x_a_emb, q_ids, a_ids, q_att_mask, 
                a_att_mask), target

    def __len__(self):
        return len(self.question_ids)


class TextDataset3(Dataset):

    def __init__(self, x_features, question_ids, answer_ids, idxs, targets=None):
        self.question_ids = question_ids[idxs].astype(np.long)
        self.answer_ids = answer_ids[idxs].astype(np.long)
        self.x_features = x_features[idxs].astype(np.float32)
        if targets is not None: self.targets = targets[idxs].astype(np.float32)
        else: self.targets = np.zeros((self.x_features.shape[0], N_TARGETS), dtype=np.float32)

    def __getitem__(self, idx):
        q_ids = self.question_ids[idx]
        a_ids = self.answer_ids[idx]
        x_feats = self.x_features[idx]
        target = self.targets[idx]
        return (x_feats, q_ids, a_ids), target

    def __len__(self):
        return len(self.x_features)