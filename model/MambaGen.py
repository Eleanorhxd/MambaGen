import torch
import torch.nn as nn
import numpy as np

from modules.visual_extractor import VisualExtractor
from modules.my_encoder_decoder import EncoderDecoder as r2gen
from modules.standard_trans import EncoderDecoder as st_trans
from modules.cam_attn_con import  CamAttnCon
from modules.my_encoder_decoder import LayerNorm
from modules.old_forebacklearning import ForeBackLearning

class (MambaGen(nn.Module):
    def __init__(self, args, tokenizer, logger = None, config = None):
        super(MambaGen, self).__init__()
        self.args = args
        self.addcls = args.addcls
        self.vis = args.vis
        self.tokenizer = tokenizer
        self.visual_extractor = VisualExtractor(args, logger, config)
        self.fbl = args.fbl
        self.wmse = args.wmse
        self.attn_cam = args.attn_cam
        self.ctm = ContextualModule1D(98) #iu
        
        if self.fbl:
            #self.fore_back_learn = ForeBackLearning(fore_t=args.fore_t, back_t=args.back_t, norm=LayerNorm(self.visual_extractor.num_features))
            self.fore_back_learn = ForeBackLearning(norm=LayerNorm(self.visual_extractor.num_features))
        if self.attn_cam:
            self.attn_cam_con = CamAttnCon(method=args.attn_method, topk= args.topk, layer_id=args.layer_id, vis=args.vis)
        self.sub_back = args.sub_back
        self.records = []
        if args.ed_name == 'r2gen':
            self.encoder_decoder = r2gen(args, tokenizer)
        elif args.ed_name == 'st_trans':
            self.encoder_decoder = st_trans(args, tokenizer)
        else:
            raise NotImplementedError
        # if args.dataset_name == 'iu_xray':
        #     self.forward = self.forward_iu_xray
        # else:
        #     self.forward = self.forward_mimic_cxr

    def __str__(self):
        model_parameters = filter(lambda p: p.requires_grad, self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        return super().__str__() + '\nTrainable parameters: {}'.format(params)

  

    def forward(self, images, targets=None,labels=None, mode='train'):# update_opts=update_opts这些额外添加
        fore_map, total_attns, weights, attns, idxs, align_attns_train = None, None, None, None, None, None
        clip_loss, logits = None, None
        if self.addcls:
            
            patch_feats, gbl_feats, logits, cams = self.visual_extractor(images)

            # patch_feats = self.ctm(patch_feats)
            patch_feats = self.cga(patch_feats)
            # print('patch_feats:', patch_feats.shape) #(32,98,1024)
            # print('gbl_feats:', gbl_feats.shape) #(32,1024)
            # print('logits:',logits.shape)#(32,14)
            # print('cams:',cams.shape)#(32,14,98)
            
            #if self.fbl and labels is not None:
            if self.fbl:
                fore_rep, back_rep, fore_map = self.fore_back_learn(patch_feats, cams, logits)
                if self.sub_back:
                    patch_feats = patch_feats - back_rep
                patch_feats = torch.cat((fore_rep, patch_feats), dim=1)

        else:
            patch_feats, gbl_feats = self.visual_extractor(images)
        if mode == 'train':
            output, fore_rep_encoded, target_embed, align_attns, clip_loss = self.encoder_decoder(gbl_feats, patch_feats, targets, mode='forward')
            if self.addcls and self.attn_cam:
                total_attns, idxs, align_attns_train = self.attn_cam_con(fore_rep_encoded, target_embed, align_attns, targets)
                # print(weights)
        elif mode == 'sample':
            output, _, attns = self.encoder_decoder(gbl_feats, patch_feats, mode='sample')
            # output = None
        else:
            raise ValueError
        if mode == 'train':
            if self.addcls:
                return output, logits, cams, fore_map, total_attns, idxs, align_attns_train, clip_loss
            else:
                return output, clip_loss
        # return output, attns
        
        return output, attns, logits



