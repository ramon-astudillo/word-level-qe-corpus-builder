import codecs
import os


def read_raw(file_path):
    with codecs.open(file_path, 'r', 'utf-8') as fid:
        sids = []
        source_sents = []
        mt_sents = []
        pe_sents = []
        ref_sents = []
        for line in fid.readlines():
            sid, source_sent, mt_sent, pe_sent, ref_sent = line.split('\t')[:5]
            # Append
            sids.append(sid)
            source_sents.append(source_sent)
            mt_sents.append(mt_sent)
            pe_sents.append(pe_sent)
            ref_sents.append(ref_sent)

    return sids, source_sents, mt_sents, pe_sents, ref_sents


def write_file(file_path, sentences):
    with codecs.open(file_path, 'w', 'utf-8') as fid:
        for sent in sentences:
            fid.write('%s\n' % sent)


def idsort(sentences, ids, target_ids):
    sents_by_id = {id: sent for id, sent in zip(ids, sentences)}
    return [sents_by_id[id] for id in target_ids]


def convert_corpus(raw_file, out_folder, label, sort_sids=None):
    if not os.path.isdir(out_folder):
        os.makedirs(out_folder)
    sids, src_sents, mt_sents, pe_sents, ref_sents = read_raw(raw_file)
    if sort_sids is not None:
        write_file('%s/%s.src' % (out_folder, label), idsort(src_sents, sids, sort_sids))
        write_file('%s/%s.mt' % (out_folder, label), idsort(mt_sents, sids, sort_sids))
        write_file('%s/%s.pe' % (out_folder, label), idsort(pe_sents, sids, sort_sids))
        write_file('%s/%s.ref' % (out_folder, label), idsort(ref_sents, sids, sort_sids))
    else:
        write_file('%s/%s.src' % (out_folder, label), src_sents)
        write_file('%s/%s.mt' % (out_folder, label), mt_sents)
        write_file('%s/%s.pe' % (out_folder, label), pe_sents)
        write_file('%s/%s.ref' % (out_folder, label), ref_sents)
    print('%s -> %s' % (raw_file, out_folder))


if __name__ == '__main__':

    # Normal set
    for sset in ['train', 'dev', 'test']:
        for language_engine in [
            'de-en.smt', 'en-cs.smt', 'en-de.nmt', 'en-de.smt', 'en-lv.nmt',
            'en-lv.smt'
        ]:
            # WMT2018/RAW/de-en.smt.test.pre-processed_final
            raw_file = '../DATA/WMT2018/RAW/%s.%s.pre-processed_final' % (language_engine, sset)
            out_folder = '../DATA/WMT2018/task2_%s_%s/' % (language_engine, sset)
            convert_corpus(raw_file, out_folder, sset)

    # Num normalized set
    for sset in ['train', 'dev', 'test']:
        raw_file = '../DATA/WMT2018/NUM_PREPRO/RAW/en-lv.nmt.%s.fully-pre-processed_final' % sset
        out_folder = '../DATA/WMT2018/NUM_PREPRO/task2_en-lv.nmt_%s/' % sset
        #ref_ids = read_raw('../DATA/WMT2018/RAW/en-lv.nmt.%s.pre-processed_final' % sset)[0]
        # convert_corpus(raw_file, out_folder, sset, sort_sids=ref_ids)
        convert_corpus(raw_file, out_folder, sset)
