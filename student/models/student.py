# -*- coding: utf-8 -*-

from odoo import models, fields, api

class student(models.Model):
    _name="student.info"
    name=fields.Char(string="firstname")
    lnmae=fields.Char(string="lastname")
    class_grade=fields.Char(string="class_grade")
    gender= fields.Selection([('male','Male'),('female','Female')],'Gender')
    roll_id=fields.Integer(string="roll_id")
    # subject=fields.Many2one("res.partner")
    # subject=fields.Many2one("subject.info",string="subject_record")
    subject_line=fields.One2many("subject.info",'student_id',string="subject")

class subject_Many(models.Model):
    _name="subject.info"


    subject_names=fields.Char(string="Subject Name")

    student_id=fields.Many2one("student.info")


