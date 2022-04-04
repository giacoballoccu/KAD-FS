import csv
import gzip
import os
from utils import *
class PGPR2KGAT(object):
    def __init__(self, args):
        self.dataset = args.dataset
        self.target_dir = MODEL_DIR_NAME[args.to]
        self.generate_user_list()
        self.generate_entity_list()
        self.generate_kg_final()
        self.generate_train_test()
        #self.encode_words_as_relation()

    def encode_words_as_relation(self):
        pid_words = {}
        main_product, _ = MAIN_PRODUCT_INTERACTION[self.dataset]
        for uid, pids in self.uid_pid_words.items():
            for pid, words in pids.items():
                pid = self.PGPR_kgid2kgat_kgid[main_product][pid]
                if pid not in pid_words: pid_words[pid] = []
                pid_words[pid].extend([self.PGPR_kgid2kgat_kgid['vocab'][int(word)] for word in words.split(" ")])

        kg_file = open(self.target_dir + DATASET_DIR_NAME[self.dataset] + "kg_final.txt", 'a')
        writer = csv.writer(kg_file, delimiter=" ")
        for pid, words in pid_words.items():
            for word in words:
                writer.writerow([pid, self.word_relation_number, word])
        kg_file.close()

    def generate_train_test(self):
        directory_str = MODEL_DIR_NAME[PGPR] + DATASET_DIR_NAME[self.dataset]
        main_product, main_relation = MAIN_PRODUCT_INTERACTION[self.dataset]
        #Read train
        file_train = gzip.open(directory_str + "train.txt.gz", 'rt')
        reader = csv.reader(file_train, delimiter="\t")
        self.uid_pid_words = {}
        uid_pids_train = {}
        uid_pids_test = {}
        for row in reader:
            uid = int(row[0])
            pid = self.PGPR_kgid2kgat_kgid[main_product][int(row[1])]
            if uid not in uid_pids_train: uid_pids_train[uid] = []
            uid_pids_train[uid].append(pid)
            if uid not in self.uid_pid_words: self.uid_pid_words[uid] = {}
            self.uid_pid_words[uid][pid] = row[2]
        file_train.close()

        file_test = gzip.open(directory_str + "test.txt.gz", 'rt')
        reader = csv.reader(file_test, delimiter="\t")
        for row in reader:
            uid = int(row[0])
            pid = self.PGPR_kgid2kgat_kgid[main_product][int(row[1])]
            if uid not in uid_pids_test: uid_pids_test[uid] = []
            uid_pids_test[uid].append(pid)
        file_test.close()

        #Write train
        file_train = open(self.target_dir + DATASET_DIR_NAME[self.dataset] + "train.txt", 'w+')
        writer = csv.writer(file_train, delimiter=" ")
        for uid, pids in uid_pids_train.items():
            writer.writerow([uid, *pids])
        file_train.close()

        #Write test
        file_test = open(self.target_dir + DATASET_DIR_NAME[self.dataset] + "test.txt", 'w+')
        writer = csv.writer(file_test, delimiter=" ")
        for uid, pids in uid_pids_test.items():
            writer.writerow([uid, *pids])
        file_test.close()

    def generate_user_list(self):
        directory_str = MODEL_DIR_NAME[PGPR] + DATASET_DIR_NAME[self.dataset]
        filei = gzip.open(directory_str + "entities/users.txt.gz", 'rt')
        fileo_path = self.target_dir + DATASET_DIR_NAME[self.dataset]
        ensure_dir(fileo_path)
        fileo = open(fileo_path + 'user_list.txt', 'w+')
        reader = csv.reader(filei, delimiter="\t")
        header = next(reader, None)
        writer = csv.writer(fileo, delimiter=" ")
        writer.writerow(header)
        for idx, row in enumerate(reader):
            writer.writerow([row[0], idx])
        filei.close()
        fileo.close()

    def generate_kg_final(self):
        directory_str = MODEL_DIR_NAME[PGPR] + DATASET_DIR_NAME[self.dataset] + "relations/"
        directory = os.fsencode(directory_str)
        relation_list = {}
        relation_counter = 0
        main_product, main_relation =  MAIN_PRODUCT_INTERACTION[self.dataset]
        kg_final_file = open(self.target_dir + DATASET_DIR_NAME[self.dataset] + "kg_final.txt", "w+")
        writer = csv.writer(kg_final_file, delimiter=" ")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            relation_name = filename.split(".")[0]
            relation_list[relation_name] = relation_counter
            relation_counter += 1
            entity_name = ENTITY_FROM_RELATION_FILE[self.dataset][relation_name]
            filei = gzip.open(directory_str + filename, 'rt')
            reader = csv.reader(filei, delimiter=" ")
            next(reader, None)
            for pid, row in enumerate(reader):
                kgat_pid = self.PGPR_kgid2kgat_kgid[main_product][pid]
                kgat_relations = [self.PGPR_kgid2kgat_kgid[entity_name][int(eid)] for eid in row]
                for kgat_eid in kgat_relations:
                    writer.writerow([kgat_pid, relation_list[relation_name], kgat_eid])
        kg_final_file.close()

        #relation_list_file = open(self.target_dir + DATASET_DIR_NAME[self.dataset] + "relation_list.txt", 'w+')
        #writer = csv.writer(relation_list_file, delimiter=" ")
        #writer.writerow(["org_id", "remap_id"])
        #for relation_name, relation_number in relation_list.items():
        #    writer.writerow([relation_name, relation_number])
        #self.word_relation_number = relation_number + 1
        #writer.writerow(["described_as", self.word_relation_number])
        #relation_list_file.close()

    def generate_entity_list(self):
        entities_eid = {}
        self.PGPR_kgid2kgat_kgid = {} # {entity_type: {pgpr_kgid: kgat_kgid}}
        dataset_eid2PGPR_kgid = {} # dataset_eid: pgpr_kgid
        main_entity = MAIN_PRODUCT_INTERACTION[self.dataset][0]
        #Collect all the entities original names/eid in the same list
        directory_str = MODEL_DIR_NAME[PGPR] + DATASET_DIR_NAME[self.dataset] + "entities/"
        directory = os.fsencode(directory_str)
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            entity_name = filename.split(".")[0]
            if entity_name == "users" or entity_name == "vocab": continue
            self.PGPR_kgid2kgat_kgid[entity_name] = {}  # {entity_type: {pgpr_kgid: kgat_kgid}}
            filei = gzip.open(directory_str + filename, 'rt')
            reader = csv.reader(filei, delimiter="\t")
            for idx, row in enumerate(reader):
                entity = row[0] if len(row) > 0 else ""
                if entity_name not in dataset_eid2PGPR_kgid: dataset_eid2PGPR_kgid[entity_name] = {}
                dataset_eid2PGPR_kgid[entity_name][entity] = idx
                if entity_name not in entities_eid: entities_eid[entity_name] = []
                entities_eid[entity_name].append(entity)
            filei.close()


        # Collect products
        products_pid = []
        products_path = MODEL_DIR_NAME[PGPR] + DATASET_DIR_NAME[self.dataset] + "entities/" + MAIN_PRODUCT_INTERACTION[self.dataset][0] + ".txt.gz"
        filei = gzip.open(products_path, 'rt')
        reader = csv.reader(filei, delimiter="\t")
        for row in reader:
            eid = row[0]
            products_pid.append(eid)
        filei.close()



        #Create the entity list file
        fileo_path = self.target_dir + DATASET_DIR_NAME[self.dataset]
        ensure_dir(fileo_path)
        fileo = open(fileo_path + 'entity_list.txt', 'w+')
        writer_entity = csv.writer(fileo, delimiter=" ")
        writer_entity.writerow(["org_id", "remap_id"])
        file_item = open(fileo_path + 'item_list.txt', 'w+')
        writer_item = csv.writer(file_item, delimiter=" ")
        writer_item.writerow(["org_id", "remap_id"])

        pid_idx = 0
        for pid in products_pid:
            pgpr_kgid = dataset_eid2PGPR_kgid[main_entity][pid]
            self.PGPR_kgid2kgat_kgid[main_entity][pgpr_kgid] = pid_idx #very important kgat start from 1 to n
            writer_entity.writerow([pid, pid_idx])
            writer_item.writerow([pid_idx, pid_idx, pid])
            pid_idx += 1

        for entity_name, entities in entities_eid.items():
            for entity in entities:
                if entity_name == "product": continue
                pgpr_kgid = dataset_eid2PGPR_kgid[entity_name][entity]
                self.PGPR_kgid2kgat_kgid[entity_name][pgpr_kgid] = pid_idx #very important kgat start from 1 to n since use 0 as placeholder
                writer_entity.writerow([entity, pid_idx])
                pid_idx += 1

        fileo.close()


