# -*- coding: utf-8 -*-
# Copyright (C) 2023-2024 TUD | ZIH
# ralf.klammer@tu-dresden.de

import logging

import jinja2
import os
import shutil

from .util import prepare_path, get_files
from .tei import TEIParser
from .yaml import CollectionConfig

log = logging.getLogger(__name__)


class CollectionModeler(object):
    def __init__(
        self,
        subproject,
        projectpath,
        templates=None,
        *args,
        **kw,
    ):
        self.subproject = subproject

        self.load_configs()
        self.in_path = self.subproject["inpath"]
        self.out_path = prepare_path(self.subproject["outpath"], create=True)
        if templates:
            templateLoader = jinja2.FileSystemLoader(searchpath=templates)
        else:
            templateLoader = jinja2.PackageLoader("tg_model", "templates")
        self.templateEnv = jinja2.Environment(
            loader=templateLoader, trim_blocks=True, lstrip_blocks=True
        )
        # add python function to jinja envirionment
        self.templateEnv.globals.update(all=all, any=any)
        self._attributes = None

    def load_configs(self):
        self.collection_config = CollectionConfig(
            projectpath=self.subproject["basepath"]
        )
        if self.collection_config.get_missing_params():
            raise Exception(
                "Missing config values for collection.yaml: %s"
                % ", ".join(self.collection_config.get_missing_params())
            )

    def render_collection(self):
        self.render_collection_base()
        self.render_collection_meta()
        self.render_edition()

    def render(self, output, content, templatefile):
        template = self.templateEnv.get_template(templatefile)
        log.debug(output)
        with open(output, "w") as f:
            f.write(template.render(content))

    def render_collection_base(self):
        files = get_files(self.in_path, as_tuple=True)
        self.render(
            "%s/%s.collection"
            % (
                self.out_path,
                # TODO: this is not the correct way to request the short title!
                self.collection_config.get("title", "collection")["short"],
            ),
            {
                **self.collection_config.content,
                "files": [file[1].replace(".xml", "") for file in files],
            },
            "{{ collection }}.collection",
        )

    def render_collection_meta(self):
        self.render(
            "%s/%s.collection.meta"
            % (
                self.out_path,
                # TODO: this is not the correct way to request the short title!
                self.collection_config.get("title", "collection")["short"],
            ),
            self.collection_config.get_dict(),
            "{{ collection }}.collection.meta",
        )

    def render_edition(self):
        files = get_files(self.in_path, as_tuple=True)
        for path, filename in files:
            tei_file = TEIParser(path=path, filename=filename)
            tei_file.set_config(self.collection_config)

            # create one directory for each file, which will contain all
            # related files afterwards
            file_path = prepare_path(
                "/".join([self.out_path, tei_file.pure_filename]),
                create=True,
            )

            self.render_edition_base(tei_file, file_path)
            self.render_edition_meta(tei_file, file_path)
            self.render_edition_work(tei_file, file_path)

    def render_edition_base(self, tei_file, file_path):
        # add one *.edition file per source file
        self.render(
            "%s/%s.edition" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.edition",
        )

    def render_edition_meta(self, tei_file, file_path):
        # add one *.edtion.meta file per source file
        self.render(
            "%s/%s.edition.meta" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.edition.meta",
        )

    def render_edition_work(self, tei_file, file_path):
        # add *.work file
        self.render(
            "%s/%s.work" % (file_path, tei_file.pure_filename),
            {},
            "{{ id }}.work",
        )
        # add *.work.meta file
        self.render(
            "%s/%s.work.meta" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.work.meta",
        )

        # add original TEI file as *.xml
        shutil.copyfile(
            tei_file.fullpath,
            f"{os.path.join(file_path, tei_file.pure_filename)}.xml",
        )

        # add *.xml.meta file
        self.render(
            "%s/%s.xml.meta" % (file_path, tei_file.pure_filename),
            tei_file.get_attributes(),
            "{{ id }}.xml.meta",
        )
